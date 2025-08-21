from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from bson import ObjectId
import json

from tools.search_tool import search_tool as recommender_tool

# Chargement des variables d'environnement
load_dotenv()


    # Logique de recommandation ici


# ================================
# INITIALISATION FASTAPI
# ================================
app = FastAPI(
    title="BH Assurance API",
    description="API pour le système de recommandation d'assurances",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# MODÈLES PYDANTIC
# ================================
class Recommendation(BaseModel):
    client_ref: str
    raisonnement: str = ""   # <= ajouté
    products: List[dict] = Field(default_factory=list)
    donnees_manquantes: str
    created_at: datetime = Field(default_factory=datetime.now)

class ChatMessage(BaseModel):
    role: str  # "user" ou "assistant"
    content: str

class ChatRequest(BaseModel):
    client_ref: str
    message: str

class ChatResponse(BaseModel):
    response: str


# ================================
# CONFIGURATIONS
# ================================
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME")
OPENROUTER_API_KEY = os.getenv("deepseekkey")

# ================================
# UTILITAIRES MONGO DB
# ================================
def get_mongodb_client():
    try:
        client = MongoClient(MONGODB_URI)
        client.admin.command("ping")
        return client
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de connexion MongoDB: {str(e)}")


from pymongo import MongoClient

def update_status(client_ref: str, new_status: str):
    """
    Met à jour l'attribut 'status' d'un document MongoDB
    en fonction du client_ref.
    
    Args:
        client_ref (str): La référence du client
        new_status (str): Le nouveau statut à appliquer
    """

    try:
        # Connexion MongoDB (adapter l'URI si besoin)
        client = get_mongodb_client()
        db = client[MONGODB_DBNAME]  
        collection = db["client_recommendations"]        # Nom de la collection

        # Mise à jour
        result = collection.update_one(
            {"client_ref": client_ref},       # Filtre
            {"$set": {"status": new_status}}  # Nouvelle valeur
        )
        if result.matched_count > 0:
            print(f"✅ Status mis à jour pour client_ref={client_ref} → {new_status}")
        else:
            print(f"⚠️ Aucun document trouvé pour client_ref={client_ref}")

    except Exception as e:
        print("❌ Erreur lors de la mise à jour :", e)

    finally:
        client.close()

# ================================

# METTRE À JOUR LE PRODUIT RECOMMANDÉ
def update_produit(client_ref: str, produit_recommande: str):
    """
    Met à jour l'attribut 'recommendation.produit_recommande' d'un document MongoDB
    en fonction du client_ref.
    
    Args:
        client_ref (str): La référence du client
        produit_recommande (str): Le nouveau produit recommandé
    """

    try:
        # Connexion MongoDB (adapter l'URI si besoin)
        client = get_mongodb_client()
        db = client[MONGODB_DBNAME]  
        collection = db["client_recommendations"]

        # Mise à jour
        result = collection.update_one(
            {"client_ref": client_ref},       
            {
                "$set": {
                    "recommendation.produit_recommande": produit_recommande,
                    "updated_at": datetime.utcnow()
                }
            }
        )

        if result.matched_count > 0:
            print(f"✅ produit mis à jour pour client_ref={client_ref} → {produit_recommande}")
        else:
            print(f"⚠️ Aucun document trouvé pour client_ref={client_ref}")

    except Exception as e:
        print("❌ Erreur lors de la mise à jour :", e)

    finally:
        client.close()

def get_client_recommendation(client_ref: str):
    try:
        client = get_mongodb_client()
        db = client[MONGODB_DBNAME]
        collection = db["client_recommendations"]
        # Recherche de la dernière recommandation pour le client
        doc = collection.find_one({"client_ref": client_ref},sort=[("created_at", -1)])
        client.close()
        
        if not doc:
            raise HTTPException(status_code=404, detail="Aucune recommandation trouvée pour ce client")
        
        # Conversion des champs MongoDB
        doc['_id'] = str(doc['_id'])
        rec=doc.get("recommendation", {})
        doc["raisonnement"] = rec.get("raisonnement", "")
        doc["donnees_manquantes"] = rec.get("donnees_manquantes", "")
        produits = rec.get("produit_recommande", [])
        if isinstance(produits, str):
            produits = [{"name": produits}]  # tu l'enveloppes dans un dict
        elif isinstance(produits, list):
            produits = [{"name": p} if isinstance(p, str) else p for p in produits]

        doc["products"] = produits
        if 'created_at' not in doc:
            doc['created_at'] = datetime.now()
        
        return Recommendation(**doc)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# ================================
# UTILITAIRES MONGO DB POUR HISTORIQUE
# ================================
def save_chat_message(client_ref: str, role: str, content: str):
    """Enregistre un message dans MongoDB"""
    client = get_mongodb_client()
    db = client[MONGODB_DBNAME]
    collection = db["history_chat"]

    doc = {
        "client_ref": client_ref,
        "role": role,
        "content": content,
        "created_at": datetime.now()
    }
    collection.insert_one(doc)
    client.close()

def get_last_chat_history(client_ref: str, limit: int = 5) -> List[dict]:
    """Récupère les derniers messages d'un client"""
    client = get_mongodb_client()
    db = client[MONGODB_DBNAME]
    collection = db["history_chat"]

    cursor = collection.find({"client_ref": client_ref}).sort("created_at", -1).limit(limit)
    messages = list(cursor)
    client.close()

    # On retourne sous format LLM-compatible
    return [
        {"role": msg["role"], "content": msg["content"]}
        for msg in reversed(messages)  # on inverse pour avoir ordre chronologique
    ]

# ================================
# MÉMOIRE EN RAM POUR LES SESSIONS
# ================================
session_histories = {}  # { client_ref: [messages] }

def get_session_history(client_ref: str) -> List[dict]:
    """Retourne l'historique de la session en mémoire, sinon charge depuis MongoDB"""
    if client_ref not in session_histories:
        # Première fois => on charge depuis MongoDB
        last_history = get_last_chat_history(client_ref, limit=5)
        session_histories[client_ref] = last_history
    return session_histories[client_ref]

def add_message_to_session(client_ref: str, role: str, content: str):
    """Ajoute un message en mémoire + DB"""
    if client_ref not in session_histories:
        session_histories[client_ref] = []
    session_histories[client_ref].append({"role": role, "content": content})
    save_chat_message(client_ref, role, content)  # on continue à persister en DB


# ================================
# CONFIGURATION LLM
# ================================
def get_llm_chat():
    return ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        model="deepseek/deepseek-chat-v3-0324:free",
        temperature=0.7,
    )

# ================================
# ENDPOINTS API
# ================================
@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    try:
        # Récupération de la recommandation
        recommendation = get_client_recommendation(request.client_ref)
        
        # Convert recommendation to dict and handle datetime serialization
        recommendation_dict = recommendation.dict()
        recommendation_dict['created_at'] = recommendation_dict['created_at'].isoformat()

        # Préparation du système prompt
        conversation_history = [
            {
                "role": "system",
                "content": (
                    "Tu es un conseiller en assurance avec 30 ans d'expérience. "
                    "Tu dois discuter avec le client, répondre à ses questions "
                    "et t'appuyer sur les données sauvegardées dans MongoDB. "
                    "Si des informations manquent, demande-les. "
                    f"Voici les informations connues sur ce client :\n\n{json.dumps(recommendation_dict, indent=2, ensure_ascii=False)}\n\n."
                    "-Si le client demande une autre recommandation, appelle le tool recommender_tool et génère un pitch commercial convaincant."
                    "-Si tu détectes de nouvelles infos pertinentes, demande si le client veut une autre recommandation."
                    "-Si le client n'est pas satisfait, demande pourquoi, puis propose une autre recommandation avec le tool."
                    "-utilise le tool update_status pour mettre à jour le statut de la recommandation si le client il vous dit qui est interssisé par le produit recommandé et il veux acheter."
                    "Si une réponse n'est pas dans les données, explique que tu ne peux pas répondre précisément."
                    "Toujours répondre de manière polie et professionnelle."
                )
            }
        ]

        # Charger les 10 derniers messages de la DB
        last_history = get_session_history(request.client_ref)
        conversation_history.extend(last_history)

        # Ajouter le message utilisateur
        conversation_history.append({"role": "user", "content": request.message})
        add_message_to_session(request.client_ref, "user", request.message)  # Sauvegarder en DB

        # Appel au LLM
        try:
            llm = get_llm_chat()
            tools = [recommender_tool, update_status]
            agent = create_react_agent(llm, tools=tools)

            response = agent.invoke({"messages": conversation_history})
            assistant_message = response["messages"][-1].content

        except Exception as e:
            try:

                llm=ChatOpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=os.getenv("deepseekkey_yahya"),
                    model="deepseek/deepseek-chat-v3-0324:free",
                    temperature=0.7,
                )
                tools = [recommender_tool, update_status]
                agent = create_react_agent(llm, tools=tools)

                response = agent.invoke({"messages": conversation_history})
                assistant_message = response["messages"][-1].content


            except Exception as e2:
                raise HTTPException(status_code=500, detail=f"Erreur LLM: {str(e2)}")

        # Sauvegarder la réponse de l'assistant
        add_message_to_session(request.client_ref, "assistant", assistant_message)

        # Retourner uniquement la dernière réponse (pas tout l’historique)
        return ChatResponse(
            response=assistant_message
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du chat: {str(e)}")

# ================================
# POINT D'ENTRÉE
# ================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)