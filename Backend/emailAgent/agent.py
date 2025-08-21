# assurance_email_agent.py
import os
import time
import imaplib
import email
import requests
import json
import re
import logging
from email.header import decode_header
from datetime import datetime
from enum import Enum
from typing import Optional
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration
class Config:
    # Email configuration
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    IMAP_SERVER = "imap.gmail.com"
    IMAP_PORT = 993
    
    # OpenRouter configuration
    OPENROUTER_API_KEY = os.getenv('deepseekkey')
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    # MongoDB configuration
    MONGODB_URI = os.getenv('MONGODB_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    
    # Models
    LLM_MODEL = "deepseek/deepseek-chat-v3-0324:free"
    
    # Check intervals
    CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', 5))

# Enum pour les statuts des clients
class ClientStatus(str, Enum):
    PROSPECT = "prospect"
    INTERESSE = "intéressé"
    NON_INTERESSE = "non_intéressé"
    CLIENT = "client"
    EN_NEGOCIATION = "en_négociation"

# Service de base de données
class DatabaseService:
    def __init__(self):
        self.client = None
        self.db = None
        self.clients_collection = None
        self.connect()
    
    def connect(self):
        """Établit la connexion à MongoDB"""
        try:
            self.client = MongoClient(Config.MONGODB_URI)
            self.db = self.client[Config.DATABASE_NAME]
            self.clients_collection = self.db['client_recommendation']
            logging.info("Connexion à MongoDB réussie")
        except PyMongoError as e:
            logging.error(f"Erreur de connexion MongoDB: {e}")
            raise
    
    def update_client_status(self, email: str, new_status: str, response_content: str = None):
        """Met à jour le statut d'un client et ajoute l'historique"""
        try:
            update_data = {
                '$set': {
                    'status': new_status,
                    'date_dernier_contact': datetime.now()
                },
                '$push': {
                    'historique_emails': {
                        'date': datetime.now(),
                        'type': 'réponse',
                        'contenu': response_content[:500] if response_content else ''  # Limiter la taille
                    }
                }
            }
            
            result = self.clients_collection.update_one(
                {'email': email},
                update_data
            )
            
            if result.modified_count > 0:
                logging.info(f"Statut mis à jour pour {email}: {new_status}")
                return True
            else:
                logging.warning(f"Client non trouvé avec l'email: {email}")
                return False
                
        except PyMongoError as e:
            logging.error(f"Erreur MongoDB lors de la mise à jour: {e}")
            return False
    
    def get_client_by_email(self, email: str):
        """Récupère un client par son email"""
        try:
            client_data = self.clients_collection.find_one({'email': email})
            return client_data
        except PyMongoError as e:
            logging.error(f"Erreur MongoDB lors de la récupération: {e}")
            return None
    
    def close_connection(self):
        """Ferme la connexion à la base de données"""
        if self.client:
            self.client.close()
            logging.info("Connexion MongoDB fermée")

# Processeur LLM pour analyse des réponses
class LLMProcessor:
    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.api_url = Config.OPENROUTER_URL
        self.model = Config.LLM_MODEL
    
    def analyze_email_response(self, email_content: str) -> dict:
        """
        Analyse le contenu d'un email de réponse pour déterminer l'intention
        et le statut approprié
        """
        # Nettoyer le contenu de l'email
        cleaned_content = email_content.strip()[:2000]  # Limiter la taille
        
        prompt = f"""
        Analyse cette réponse email d'un client d'assurance et détermine:
        1. L'intention du client (intéressé, non intéressé, demande d'information)
        2. Le statut approprié à assigner
        
        Réponse email:
        {cleaned_content}
        
        Réponds UNIQUEMENT au format JSON avec:
        {{
            "intention": "intéressé|non_intéressé|information",
            "statut_recommande": "intéressé|non_intéressé|en_négociation|prospect",
            "confiance": 0.0-1.0,
            "raison": "explication courte"
        }}
        """
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': self.model,
                'messages': [
                    {
                        'role': 'system',
                        'content': 'Tu es un assistant expert en analyse de réponses clients pour une compagnie d\'assurance. Réponds uniquement en JSON.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.1,
                'max_tokens': 500
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            llm_response = result['choices'][0]['message']['content']
            
            # Nettoyer et parser la réponse JSON
            llm_response = llm_response.strip().replace('```json', '').replace('```', '').strip()
            analysis = json.loads(llm_response)
            
            logging.info(f"Analyse LLM réussie: {analysis}")
            return analysis
            
        except Exception as e:
            logging.error(f"Erreur lors de l'analyse LLM: {e}")
            # Fallback en cas d'erreur
            return {
                "intention": "information",
                "statut_recommande": "prospect",
                "confiance": 0.5,
                "raison": "Erreur d'analyse, statut par défaut"
            }
    
    def map_status(self, status_str: str) -> ClientStatus:
        """Mappe le statut string vers l'enum ClientStatus"""
        status_mapping = {
            'intéressé': ClientStatus.INTERESSE,
            'non_intéressé': ClientStatus.NON_INTERESSE,
            'en_négociation': ClientStatus.EN_NEGOCIATION,
            'prospect': ClientStatus.PROSPECT,
            'client': ClientStatus.CLIENT
        }
        return status_mapping.get(status_str.lower(), ClientStatus.PROSPECT)

# Récepteur d'emails
class EmailReceiver:
    def __init__(self):
        self.imap = None
        self.llm_processor = LLMProcessor()
        self.db_service = DatabaseService()
        self.connected = False
    
    def connect(self):
        """Établit la connexion IMAP"""
        try:
            self.imap = imaplib.IMAP4_SSL(Config.IMAP_SERVER, Config.IMAP_PORT)
            self.imap.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
            self.connected = True
            logging.info("Connexion IMAP réussie")
            return True
        except Exception as e:
            logging.error(f"Erreur de connexion IMAP: {e}")
            self.connected = False
            return False
    
    def check_responses(self):
        """Vérifie les nouvelles réponses et les traite"""
        if not self.connected:
            if not self.connect():
                return
        
        try:
            self.imap.select('INBOX')
            
            # Chercher les emails non lus
            status, messages = self.imap.search(None, 'UNSEEN')
            if status != 'OK':
                return
            
            email_ids = messages[0].split()
            
            if email_ids:
                logging.info(f"Found {len(email_ids)} new emails")
            
            for email_id in email_ids:
                self.process_email(email_id)
                
        except Exception as e:
            logging.error(f"Erreur lors de la vérification des emails: {e}")
            self.connected = False
    
    def process_email(self, email_id):
        """Traite un email spécifique"""
        try:
            status, msg_data = self.imap.fetch(email_id, '(RFC822)')
            if status != 'OK':
                return
            
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Extraire les informations de l'email
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')
            
            from_email = msg['From']
            body = self.extract_email_body(msg)
            
            # Vérifier si c'est une réponse à nos emails
            if self.is_response_to_our_pitch(from_email):
                email_address = self.extract_email_address(from_email)
                logging.info(f"Nouvelle réponse de {email_address}: {subject}")
                self.handle_client_response(email_address, body)
                
                # Marquer comme lu
                self.imap.store(email_id, '+FLAGS', '\\Seen')
                
        except Exception as e:
            logging.error(f"Erreur lors du traitement de l'email {email_id}: {e}")
    
    def extract_email_body(self, msg):
        """Extrait le corps textuel de l'email"""
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode(errors='ignore')
                        break
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode(errors='ignore')
            except:
                pass
        
        return body
    
    def is_response_to_our_pitch(self, from_email: str) -> bool:
        """Vérifie si l'email est une réponse à nos propositions"""
        email_address = self.extract_email_address(from_email)
        client = self.db_service.get_client_by_email(email_address)
        return client is not None
    
    def extract_email_address(self, email_header: str) -> str:
        """Extrait l'adresse email pure depuis le header"""
        match = re.search(r'<(.+?)>', email_header)
        if match:
            return match.group(1)
        
        # Fallback: chercher un pattern email simple
        match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', email_header)
        if match:
            return match.group(1)
        
        return email_header
    
    def handle_client_response(self, email_address: str, response_content: str):
        """Traite la réponse du client"""
        try:
            # Analyser la réponse avec LLM
            analysis = self.llm_processor.analyze_email_response(response_content)
            
            # Mapper le statut
            new_status = self.llm_processor.map_status(analysis['statut_recommande'])
            
            # Mettre à jour la base de données
            success = self.db_service.update_client_status(
                email_address, 
                new_status.value, 
                response_content
            )
            
            if success:
                logging.info(f"Client {email_address} mis à jour vers: {new_status.value}")
                logging.info(f"Raison: {analysis['raison']} (confiance: {analysis['confiance']})")
            else:
                logging.warning(f"Échec de la mise à jour pour {email_address}")
            
        except Exception as e:
            logging.error(f"Erreur lors du traitement de la réponse: {e}")
    
    def disconnect(self):
        """Ferme toutes les connexions"""
        try:
            if self.imap:
                self.imap.logout()
            self.db_service.close_connection()
            logging.info("Toutes les connexions fermées")
        except Exception as e:
            logging.error(f"Erreur lors de la fermeture: {e}")

# Application principale
def main():
    """Application principale"""
    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('assurance_agent.log')
        ]
    )
    
    logging.info("Démarrage de l'agent de gestion des réponses emails...")
    
    email_receiver = EmailReceiver()
    
    if not email_receiver.connect():
        logging.error("Impossible de se connecter au serveur email")
        return
    
    # Planifier la vérification périodique des emails
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        email_receiver.check_responses,
        'interval',
        minutes=Config.CHECK_INTERVAL_MINUTES,
        id='email_check'
    )
    
    scheduler.start()
    
    try:
        logging.info(f"Agent démarré. Vérification toutes les {Config.CHECK_INTERVAL_MINUTES} minutes...")
        logging.info("Appuyez sur Ctrl+C pour arrêter")
        
        # Vérification immédiate au démarrage
        email_receiver.check_responses()
        
        # Boucle principale
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logging.info("Arrêt de l'agent...")
    except Exception as e:
        logging.error(f"Erreur inattendue: {e}")
    finally:
        scheduler.shutdown()
        email_receiver.disconnect()
        logging.info("Agent arrêté")

if __name__ == "__main__":
    main()