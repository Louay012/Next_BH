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
    history: Optional[List[ChatMessage]] = Field(default_factory=list)

class ChatResponse(BaseModel):
    response: str
    history: List[ChatMessage]

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
# CONFIGURATION LLM
# ================================
def get_llm_chat():
    return ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("deepseekkey_compte2"),
        model="deepseek/deepseek-chat-v3-0324:free",
        temperature=0.7,
    )

# ================================
# ENDPOINTS API
# ================================
@app.get("/recommendations/{client_ref}", response_model=Recommendation)
async def get_recommendations(client_ref: str):
    """
    Récupère les dernières recommandations pour un client
    """
    return get_client_recommendation(client_ref)


@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Endpoint pour discuter avec l'agent virtuel
    """
    try:
        # Récupération de la recommandation
        recommendation = get_client_recommendation(request.client_ref)
        
        # Convert recommendation to dict and handle datetime serialization
        recommendation_dict = recommendation.dict()
        recommendation_dict['created_at'] = recommendation_dict['created_at'].isoformat()

        print(recommendation_dict)
        
        # Préparation de l'historique de conversation
        conversation_history = [
            {
                "role": "system",
                "content": (
                    "Tu es un conseiller en assurance avec 30 ans d'expérience. "
                    "Tu dois discuter avec le client, répondre à ses questions "
                    "et t'appuyer sur les données sauvegardées dans MongoDB. "
                    "Si des informations manquantes, tu dois lui demander de les fournir. "
                    f"Voici les informations connues sur ce client :\n\n{json.dumps(recommendation_dict, indent=2, ensure_ascii=False)}\n\n."
                    "-Si le client demande de recommander un autre produit faire un raisonnement pour son situation et appeller tool recommender_tool et générer un bon pitch commercial pour convincre par ce nouveau produit."
                    "-Si vous trouver des nouveaux informations pertinentes depuis le client relatif a son comportement et sa vie qui nécessite un nouveau produit assurance pour covrer sa situation, vous posez la question si il veut une autre recommandation."
                    "-Si le client n'est pas satisfait de la recommandation, vous devez lui demander de préciser ce qui ne va pas et pourquoi. et demander si il veut une autre recommandation. si oui faire un raisonnement pour sa situation et appeller le tool recommender_tool et générer un bon pitch commercial pour convaincre par ce nouveau produit."
                    "Si une réponse n'est pas dans les données, explique que tu ne peux pas répondre précisément."
                    "Tu dois toujours répondre de manière polie et professionnelle."
                )
            }
        ]

        # Ajout de l'historique existant
        if request.history:
            conversation_history.extend([msg.dict() for msg in request.history])

        # Ajout du nouveau message
        conversation_history.append({"role": "user", "content": request.message})
        # Appel au LLM
       # Appel au LLM
        try:
            llm = get_llm_chat()
            tools = [recommender_tool]
            agent = create_react_agent(llm, tools=tools)

            # ⚠️ LangGraph attend {"messages": [...]}, pas juste une liste
            response = agent.invoke({"messages": conversation_history})

            # Récupération de la dernière réponse de l’assistant
            assistant_message = response["messages"][-1].content

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération du LLM: {str(e)}")

        
        conversation_history.append({"role": "assistant", "content": assistant_message})

        # Filtrage de l'historique pour la réponse (sans le système prompt)
        chat_history = [
            ChatMessage(**msg) for msg in conversation_history 
            if msg['role'] in ['user', 'assistant']
        ]

        return ChatResponse(
            response=assistant_message,
            history=chat_history
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du chat: {str(e)}")
# ================================
# ENDPOINT DE SANTÉ
# ================================


@app.get("/health")
async def health_check():
    """Endpoint de vérification de la santé de l'API"""
    try:
        # Test MongoDB
        client = get_mongodb_client()
        client.admin.command("ping")
        client.close()
        
        # Test LLM
        llm = get_llm_chat()
        test_response = llm.invoke([{"role": "user", "content": "Test"}])
        
        return {
            "status": "healthy",
            "llm_response" : test_response.content,
            "details": {
                "mongodb": "connected",
                "llm": "responsive"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

# ================================
# POINT D'ENTRÉE
# ================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)