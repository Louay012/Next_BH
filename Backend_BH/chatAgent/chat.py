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
from langchain.tools import tool

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
    Met à jour le 'status' du dernier document inséré (dernier recommendation)
    pour un client donné.
    """
    try:
        print("Connexion à MongoDB...")
        client = get_mongodb_client()
        db = client[MONGODB_DBNAME]
        collection = db["client_recommendations"]

        # Trouver le dernier document pour ce client (tri par _id décroissant)
        last_doc = collection.find_one(
            {"client_ref": client_ref}, 
            sort=[("_id", -1)]
        )

        if not last_doc:
            print(f"⚠️ Aucun document trouvé pour client_ref={client_ref}")
            return

        # Mise à jour du dernier document trouvé
        result = collection.update_one(
            {"_id": last_doc["_id"]},
            {"$set": {"status": new_status}}
        )

        if result.modified_count > 0:
            print(f"✅ Dernier status mis à jour pour client_ref={client_ref} → {new_status}")
        else:
            print(f"⚠️ La mise à jour n'a pas eu lieu (status déjà identique ?)")

    except Exception as e:
        print("❌ Erreur lors de la mise à jour :", e)

    finally:
        client.close()


# ================================

from datetime import datetime

@tool
def save_recommendation(
    client_ref: str,
    raisonnement: str,
    produit_recommande: str,
    branche: str,
    score_pertinence: str,
    pitch: str,
    conditions_generales: str,
    donnees_manquantes: str = None,
    errors: str = None
):
    """
    Enregistre une nouvelle recommandation dans MongoDB pour un client donné.
    
    Args:
        client_ref (str): La référence du client
        raisonnement (str): Analyse/raisonnement du LLM
        produit_recommande (str): Produit recommandé
        branche (str): Branche d’assurance
        score_pertinence (str): Score sur 100
        pitch (str): Pitch commercial
        conditions_generales (str): Infos CG produit
        donnees_manquantes (str, optionnel): Champs manquants détectés
        errors (str, optionnel): Erreurs éventuelles
    """
    try:
        print("Connexion à MongoDB...")
        client = get_mongodb_client()
        db = client[MONGODB_DBNAME]
        collection = db["client_recommendations"]

        # Nouveau document à insérer
        recommendation_doc = {
            "client_ref": client_ref,
            "recommendation": {
                "raisonnement": raisonnement,
                "produit_recommande": produit_recommande,
                "branche": branche,
                "score_pertinence": score_pertinence,
                "pitch": pitch,
                "conditions_generales": conditions_generales,
                "donnees_manquantes": donnees_manquantes,
                "errors": errors
            },
            "status": "proposé",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # Insertion dans MongoDB
        result = collection.insert_one(recommendation_doc)

        print(f"✅ Nouvelle recommandation enregistrée (id={result.inserted_id})")

    except Exception as e:
        print("❌ Erreur lors de l'enregistrement :", e)

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
        last_history = get_last_chat_history(client_ref, limit=2)
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
                    "Tu es un conseiller expert en assurance avec 30 ans d'expérience. "
                    "Ta mission : répondre de manière claire, concise et professionnelle aux questions du client, "
                    "en utilisant uniquement les données disponibles et les outils fournis.\n\n"

                    f"Voici les informations connues sur ce client :\n{json.dumps(recommendation_dict, indent=2, ensure_ascii=False)}\n\n"

                    "Règles importantes a appliquer , je n'accepte pas une réponse qui n'applique pas ces règles :\n"
                    "1. Si des informations sont manquantes ou incertaines, demande-les au client avant de répondre.\n"
                    "2. Si le user demande une autre recommandation ou le user n'est pas interrésé par le produit alors:"
                        "- appelle `recommender_tool` pour générer un pitch."
                        "- appelle `update_status` pour changer le statut de la dernière recommandation en 'refused'."
                        "- ensuite appelle `save_recommendation` en lui passant les champs suivants :"
                        "{client_ref, raisonnement, produit_recommande, branche, score_pertinence, pitch, conditions_generales}."
                        "Ne réponds pas au client avant d’avoir sauvegardé la recommandation."

                    "3. si le client est intéressé par le produit recommandé, appelle `update_status` pour changer le statut en 'accepté' .\n"
                    ". Utilise les outils disponibles (`recommender_tool`, `update_status`,'save_recommendation') uniquement lorsque cela est pertinent\n"
                    "tu dois l’appeler directement avec les bons arguments JSON, pas simplement le mentionner dans ta réponse.\n"
                    "tout en maintenant un dialogue interactif et compréhensible."
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
            tools = [recommender_tool, update_status, save_recommendation]
            agent = create_react_agent(llm, tools=tools)

            response = agent.invoke({"messages": conversation_history})
            assistant_message = response["messages"][-1].content

        except Exception as e:
            print("pas de réponse du LLM principal, on bascule vers le LLM de secours...")
            try:

                llm=ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("z_key"),
                model="z-ai/glm-4.5-air:free",
                temperature=0.7,
                )
                tools = [recommender_tool, update_status, save_recommendation]
                agent = create_react_agent(llm, tools=tools)

                response = agent.invoke({"messages": conversation_history})
                assistant_message = response["messages"][-1].content


            except Exception as e2:
                print("pas de réponse du LLM de secours 1, on bascule vers le LLM de secours 2...")
                try:
                    
                    """llm = ChatOllama(
                    model="llama3.1:8b",  # Modèle adapté à ta GTX + CPU i5
                    temperature=0,         # Réponses déterministes
                    base_url="http://localhost:11434"
                    )
                    tools = [recommender_tool, update_status, save_recommendation]
                    agent = create_react_agent(llm, tools=tools)
                    response = agent.invoke({"messages": conversation_history})
                    assistant_message = response["messages"][-1].content"""

                except Exception as e3:
                    raise HTTPException(status_code=500, detail=f"Erreur LLM: {str(e3)}")

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