import jwt
import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()

# Clé secrète pour signer les tokens
#SECRET_KEY = "ma_cle_secrete_super_longue"
import secrets
SECRET_KEY = secrets.token_urlsafe(64)  
print(SECRET_KEY)

# Connexion MongoDB
client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("MONGODB_DBNAME")]
tokens_collection = db["client_tokens"]

def generate_token(ref_client: str) -> str:
    """
    Génère un token JWT pour un client spécifique et l'enregistre dans MongoDB.
    
    Args:
        ref_client (str): Référence unique du client

    Returns:
        str: Token JWT généré
    """
    # Expiration du token (par ex : 24h)
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=720)

    # Création du token JWT
    payload = {
        "ref_client": ref_client,
        "exp": expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    # Sauvegarde dans MongoDB
    tokens_collection.update_one(
        {"ref_client": ref_client},
        {"$set": {
            "token": token,
            "created_at": datetime.datetime.utcnow(),
            "expires_at": expiration
        }},
        upsert=True  # Crée un nouveau doc si le client n'existe pas
    )
    print(f"Token généré pour le client {ref_client} : {token}")

    return token
print(generate_token("133546780"))