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
from tools.envoyerEmail import envoyer_email_complet  # <-- Import de la fonction d'envoi
load_dotenv()

# --- CONFIGURATION ---
class Config:
    EMAIL_USER = "fezaimohamedelamine@gmail.com"
    EMAIL_PASSWORD = "tspr mwfu cdze xdnl"  # mot de passe d'application Gmail
    IMAP_SERVER = "imap.gmail.com"
    IMAP_PORT = 993

    OPENROUTER_API_KEY = os.getenv('deepseekkey')
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

    MONGODB_URI = os.getenv('MONGODB_URI')
    DATABASE_NAME = os.getenv('MONGODB_DBNAME', 'assurance_db')

    LLM_MODEL = "deepseek/deepseek-chat-v3-0324:free"
    CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', 5))

class ClientStatus(str, Enum):
    PROSPECT = "prospect"
    INTERESSE = "intéressé"
    NON_INTERESSE = "non_intéressé"
    CLIENT = "client"
    EN_NEGOCIATION = "en_négociation"

class DatabaseService:
    def __init__(self):
        self.client = None
        self.db = None
        self.clients_collection = None
        self.emails_collection = None
        self.connect()

    def connect(self):
        try:
            self.client = MongoClient(Config.MONGODB_URI)
            self.db = self.client[Config.DATABASE_NAME]
            self.clients_collection = self.db['client_recommendation']
            self.emails_collection = self.db['client_emails']
            logging.info("Connexion à MongoDB réussie")
        except PyMongoError as e:
            logging.error(f"Erreur de connexion MongoDB: {e}")
            raise

    def update_client_status(self, email: str, new_status: str, response_content: str = None):
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
                        'contenu': response_content[:500] if response_content else ''
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
        try:
            client_data = self.clients_collection.find_one({'email': email})
            return client_data
        except PyMongoError as e:
            logging.error(f"Erreur MongoDB lors de la récupération: {e}")
            return None

    def save_processed_email(self, email_address, subject, body, summary, reply, date=None):
        try:
            doc = {
                "email": email_address,
                "subject": subject,
                "body": body[:1000],
                "summary": summary,
                "reply": reply,
                "date": date or datetime.now()
            }
            self.emails_collection.insert_one(doc)
            logging.info(f"Email stocké dans client_emails pour {email_address}")
        except PyMongoError as e:
            logging.error(f"Erreur MongoDB lors du stockage de l'email: {e}")

    def close_connection(self):
        if self.client:
            self.client.close()
            logging.info("Connexion MongoDB fermée")

class LLMProcessor:
    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.api_url = Config.OPENROUTER_URL
        self.model = Config.LLM_MODEL

    def analyze_email_response(self, email_content: str) -> dict:
        cleaned_content = email_content.strip()[:2000]
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
            llm_response = llm_response.strip().replace('```json', '').replace('```', '').strip()
            analysis = json.loads(llm_response)
            logging.info(f"Analyse LLM réussie: {analysis}")
            return analysis
        except Exception as e:
            logging.error(f"Erreur lors de l'analyse LLM: {e}")
            return {
                "intention": "information",
                "statut_recommande": "prospect",
                "confiance": 0.5,
                "raison": "Erreur d'analyse, statut par défaut"
            }

    def map_status(self, status_str: str) -> ClientStatus:
        status_mapping = {
            'intéressé': ClientStatus.INTERESSE,
            'non_intéressé': ClientStatus.NON_INTERESSE,
            'en_négociation': ClientStatus.EN_NEGOCIATION,
            'prospect': ClientStatus.PROSPECT,
            'client': ClientStatus.CLIENT
        }
        return status_mapping.get(status_str.lower(), ClientStatus.PROSPECT)

class EmailReceiver:
    def __init__(self):
        self.imap = None
        self.llm_processor = LLMProcessor()
        self.db_service = DatabaseService()
        self.connected = False

    def connect(self):
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
        if not self.connected:
            if not self.connect():
                return
        try:
            self.imap.select('INBOX')
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
        try:
            status, msg_data = self.imap.fetch(email_id, '(RFC822)')
            if status != 'OK':
                return
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')
            from_email = msg['From']
            body = self.extract_email_body(msg)
            if self.is_response_to_our_pitch(from_email):
                email_address = self.extract_email_address(from_email)
                logging.info(f"Nouvelle réponse de {email_address}: {subject}")
                self.handle_client_response(email_address, body, subject)
                self.imap.store(email_id, '+FLAGS', '\\Seen')
        except Exception as e:
            logging.error(f"Erreur lors du traitement de l'email {email_id}: {e}")

    def extract_email_body(self, msg):
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
        email_address = self.extract_email_address(from_email)
        client = self.db_service.get_client_by_email(email_address)
        return client is not None

    def extract_email_address(self, email_header: str) -> str:
        match = re.search(r'<(.+?)>', email_header)
        if match:
            return match.group(1)
        match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', email_header)
        if match:
            return match.group(1)
        return email_header

    def handle_client_response(self, email_address: str, response_content: str, subject: str):
        try:
            analysis = self.llm_processor.analyze_email_response(response_content)
            new_status = self.llm_processor.map_status(analysis['statut_recommande'])
            success = self.db_service.update_client_status(
                email_address,
                new_status.value,
                response_content
            )
            reply_body = self.generate_reply(new_status.value)
            if success:
                logging.info(f"Client {email_address} mis à jour vers: {new_status.value}")
                logging.info(f"Raison: {analysis['raison']} (confiance: {analysis['confiance']})")
                # Utilisation de la fonction d'envoi importée
                texte_complet = f"Objet : Re: {subject}\n{reply_body}"
                envoyer_email_complet(texte_complet, email_address)
            else:
                logging.warning(f"Échec de la mise à jour pour {email_address}")
            # Stockage dans client_emails (toujours, même si update échoue)
            self.db_service.save_processed_email(
                email_address=email_address,
                subject=subject,
                body=response_content,
                summary=analysis.get('raison', ''),
                reply=reply_body,
                date=datetime.now()
            )
        except Exception as e:
            logging.error(f"Erreur lors du traitement de la réponse: {e}")

    def generate_reply(self, status: str) -> str:
        if status == "intéressé":
            return "Merci pour votre intérêt ! Nous revenons vers vous rapidement pour finaliser votre dossier."
        elif status == "non_intéressé":
            return "Merci pour votre retour. Nous restons à votre disposition si besoin."
        elif status == "en_négociation":
            return "Merci pour votre réponse, nous sommes à votre écoute pour toute question complémentaire."
        else:
            return "Merci pour votre message. Nous restons à votre disposition pour toute information."

    def disconnect(self):
        try:
            if self.imap:
                self.imap.logout()
            self.db_service.close_connection()
            logging.info("Toutes les connexions fermées")
        except Exception as e:
            logging.error(f"Erreur lors de la fermeture: {e}")

def main():
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
        email_receiver.check_responses()
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