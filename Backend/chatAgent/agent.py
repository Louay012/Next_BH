import os
import json
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_openai import ChatOpenAI

# ================================
# CONFIGURATION
# ================================
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME")
OPENROUTER_API_KEY = os.getenv("deepseekkey")

# ================================
# MONGO DB UTILS
# ================================
def get_mongodb_client():
    client = MongoClient(MONGODB_URI)
    client.admin.command("ping")
    return client

def get_client_recommendation(client_ref):
    client = get_mongodb_client()
    db = client[MONGODB_DBNAME]
    collection = db["client_recommendations"]

    doc = collection.find_one({"client_ref": client_ref}, sort=[("created_at", -1)])
    client.close()
    return doc

# ================================
# LLM CONFIG
# ================================
def get_llm_chat():
    return ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        model="deepseek/deepseek-chat-v3-0324:free",
        temperature=0.7,
    )

# ================================
# CHAT AVEC LE CLIENT
# ================================
def start_chat(client_ref):
    # Récupération de la dernière recommandation sauvegardée
    recommendation_doc = get_client_recommendation(client_ref)
    if not recommendation_doc:
        print("⚠️ Aucune recommandation trouvée pour ce client.")
        return
    
    recommendation_data = recommendation_doc["recommendation"]

    # Contexte de départ
    system_prompt = {
        "role": "system",
        "content": (
            "Tu es un conseiller en assurance avec 30 ans d'expérience. "
            "Tu dois discuter avec le client, répondre à ses questions "
            "et t'appuyer sur les données sauvegardées dans MongoDB. "
            "si il ya des informations manquantes , tu dois lui demander de les fournir. "
            f"Voici les informations connues sur ce client :\n\n{json.dumps(recommendation_data, indent=2, ensure_ascii=False)}\n\n"
            "Ne jamais inventer de nouveaux produits. Si une réponse n'est pas dans les données, explique que tu ne peux pas répondre précisément."
        )
    }

    llm = get_llm_chat()
    conversation_history = [system_prompt]

    print("💬 Chat démarré. Tape 'exit' pour quitter.\n")

    while True:
        user_input = input("Client: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("👋 Fin du chat.")
            break

        conversation_history.append({"role": "user", "content": user_input})
        response = llm.invoke(conversation_history)

        assistant_message = response.content
        conversation_history.append({"role": "assistant", "content": assistant_message})

        print(f"Agent: {assistant_message}\n")


# ================================
# MAIN
# ================================
if __name__ == "__main__":
    ref = "1381"  # Exemple
    start_chat(ref)
