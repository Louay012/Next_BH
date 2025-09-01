import json
import re
import json
from dotenv import load_dotenv
import os
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from .analyseDB_tool import analyseDB
from .RAG2_tool import rag_tool
from .search_tool2 import search_tool
from .traduire_tool import translate
from .generateToken import generate_token
from .envoyerEmail import envoyer_email_complet
from .analyseSinistres import get_sinistres_client

#from pymongo import MongoClient

# Chargement variables .env
load_dotenv()


MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME")

# Connexion MongoDB
try:
    from pymongo import MongoClient
    def get_mongodb_client():
        try:
            client = MongoClient(MONGODB_URI)
            client.admin.command('ping')
            return client
        except Exception as e:
            log_message(f"Erreur de connexion MongoDB: {e}", "ERROR")
            raise

    def save_recommendation(client_ref, recommendation_data, status):
        client = get_mongodb_client()
        db = client[MONGODB_DBNAME]
        collection = db["client_recommendations"]
        
        document = {
            "client_ref": client_ref,
            "recommendation": recommendation_data,
            "status": status,
            "new_data":{},
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        try:
            result = collection.insert_one(document)
            log_message(f"Recommandation sauvegardée pour le client {client_ref} avec l'ID {result.inserted_id}", "SUCCESS")
            return str(result.inserted_id)
        except Exception as e:
            log_message(f"Erreur lors de la sauvegarde: {e}", "ERROR")
            raise
        finally:
            client.close()


except Exception as e:
    raise ValueError(f"Erreur de connexion MongoDB: {e}")

OPENROUTER_API_KEY = os.getenv("deepseekkey")
if not OPENROUTER_API_KEY:
    raise ValueError("La clé API deepseekkey n'est pas définie dans .env")




ref = "569003"


# Prompt principal


# Outils
tools = [get_sinistres_client]

# Fonction de logging
def log_message(message, role="INFO"):
    colors = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m"
    }
    reset = "\033[0m"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color = colors.get(role, "\033[0m")
    log_line = f"[{timestamp}] [{role}] {message}"
    
    # Affichage console
    print(f"{color}{log_line}{reset}")
    
    # Sauvegarde fichier
    with open("agent_logs.txt", "a", encoding="utf-8") as f:
        f.write(log_line + "\n")
def extract_json(text):
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    else:
        return None

def get_llm_deepseek():
    return ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("qween3"),
        model="qwen/qwen3-coder:free",
        temperature=0.7,
    )

def get_llm_backup():
    return ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("z_key"),
        model="z-ai/glm-4.5-air:free",
        temperature=0.7,
    )
def get_llm_backup2():
    return ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("z_key_compte2"),
        model="z-ai/glm-4.5-air:free",
        temperature=0.7,
    )


def get_agent_sinistres(client_ref):
    llm = get_llm_deepseek()
    """"llm = ChatOllama(
    model="llama3.1:8b",  # Modèle adapté à ta GTX + CPU i5
    temperature=0,         # Réponses déterministes
    base_url="http://localhost:11434",
)"""
    # Génération du token
    #client_ref="12370"
    # Prompt
    prompt = [
    {
        "role": "system",
        "content": (
            "Vous êtes un expert en assurance spécialisé dans l'analyse des sinistres. "
            "Votre mission : pour un client donné, utilisez le tool get_sinistres_client pour récupérer la liste des sinistres liés à son dernier contrat. "
            "Analysez en détail les causes, circonstances et récurrences éventuelles de ces sinistres. "
            "Réalisez un raisonnement explicite sur les causes probables, les facteurs aggravants ou récurrents, et proposez des pistes de prévention adaptées au profil du client. "
            "Ensuite, rédigez un email personnalisé (minimum 100 mots) à destination du client, expliquant votre analyse, les causes identifiées, et des conseils concrets pour éviter de futurs sinistres. "
            "L'email doit être clair, empathique, pédagogique et inciter le client à adopter de bonnes pratiques. "
            "Si aucune donnée n'est trouvée, indiquez-le honnêtement dans l'email. "
            "Le résultat final doit être au format JSON strictement, exemple :\n"
            "{\n"
            "  \"analyse\": \"...\",\n"
            "  \"causes_probables\": \"...\",\n"
            "  \"conseils_prevention\": \"...\",\n"
            "  \"email\": \"...\",\n"
            "  \"donnees_manquantes\": \"...\",\n"
            "  \"errors\": \"...\"\n"
            "}"
        )
    },
    {
        "role": "user",
        "content": (
            f"Pour le client de référence ref = {client_ref}, analyse les sinistres du dernier contrat en utilisant le tool get_sinistres_client. "
            "Explique les causes, propose des conseils de prévention, puis génère un email détaillé pour le client."
        )
    }
    ]
    agent = create_react_agent(llm, tools)
    
    try:
        log_message("Envoi de la requête à Deepseek...", "INFO")
        result = agent.invoke({"messages": prompt})
        log_message("Réponse obtenue depuis Deepseek ✅", "SUCCESS")
    except Exception as e:
        log_message(f"Erreur avec Deepseek : {e}", "WARNING")
        log_message("Bascule vers le LLM de secours...", "WARNING")
        
        llm = get_llm_backup()
        agent = create_react_agent(llm, tools)
        try:
            result = agent.invoke({"messages": prompt})
            log_message("Réponse obtenue depuis le LLM de secours ✅", "SUCCESS")
        except Exception as e:
            log_message(f"Erreur avec le LLM de secours 1: {e}", "ERROR")
            llm = get_llm_backup2()
            agent = create_react_agent(llm, tools)
            try:
                result = agent.invoke({"messages": prompt})
                log_message("Réponse obtenue depuis le LLM de secours 2 ✅", "SUCCESS")
            except Exception as e:
                log_message(f"Erreur avec le LLM de secours 2: {e}", "ERROR")
                # Si toutes les tentatives échouent, retourner une erreur
                return
    
    # Extraction de la dernière réponse AI
    messages = result.get("messages", [])
    for msg in reversed(messages):
            if hasattr(msg, "content"):
                try:
                    # Essayer de parser le contenu comme JSON

                    body_email = ""   # initialisation par défaut
                    response_text = msg.content
                    parsed_json = extract_json(response_text)
                    status= "pending"

                    if parsed_json is None:
                        parsed_json = {}  # initialise un dictionnaire vide si c'est None
                
                    #response = json.loads(msg.content)
                    # Sauvegarde dans MongoDB
                    #recommendation_id = save_recommendation(client_ref, parsed_json, status)
                        

                    #parsed_json["recommendation_id"] = recommendation_id
                    # Génération du token
                    #client_token=generate_token(client_ref)
                    # Génération du lien
                    #lien = f"http://localhost:5173/chatbot/{client_ref}"
                    body_email = parsed_json.get("email", "")
                    #body_email += f"\n\nPour plus de détails, veuillez consulter le lien suivant : {lien}"
                    #print(f"Body de l'email : {body_email}")

                    # Envoi de l'email
                    if parsed_json.get("email") not in [None, "", "Aucun"]:
                        envoyer_email_complet(body_email, "fezaimohamedelamine@gmail.com")
                    else:
                        log_message("Aucun produit adapté trouvé, email non envoyé.", "INFO")

                    return {
                        "status": "success",
                        "data": parsed_json
                    }
                except json.JSONDecodeError:
                    # Si ce n'est pas du JSON, retourner le texte brut
                    return {
                        "status": "success",
                        "data": {"response": msg.content}
                    }
        
    return {"status": "error", "message": "Aucune réponse valide trouvée"}








