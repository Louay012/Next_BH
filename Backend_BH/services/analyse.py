from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv
import os


# --- 1. Connexion MongoDB ---
def get_mongo_collection():
    load_dotenv()
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client[os.getenv("MONGODB_DBNAME")]
    return db["client_recommendations"]


# --- 2. Charger les données ---
def load_data(collection):
    docs = list(collection.find({}))
    return pd.json_normalize(docs)


def resume_recommandations():
    """
    Retourne un résumé des recommandations :
    - Nombre de produits acceptés, refusés, en cours
    - Nombre total de recommandations
    - Nombre de clients avec au moins une recommandation
    - Top 5 des produits les plus recommandés
    - Top 5 des produits les plus acceptés
    """
    df = load_data(get_mongo_collection())

    # Compter les statuts (cast en int)
    accepted = int((df["status"] == "accepté").sum())
    refused = int((df["status"] == "refusé").sum())
    pending = int((df["status"] == "en cours").sum())

    # Total des recommandations
    total_recos = int(len(df))

    # Nombre de clients avec au moins une recommandation
    clients_with_recos = int(df["client_ref"].nunique())

    # Top 5 des produits recommandés (tous statuts confondus)
    top5_recommended = (
        df["recommendation.produit_recommande"]
        .value_counts()
        .head(5)
        .to_dict()
    )

    # Top 5 des produits acceptés
    top5_accepted = (
        df[df["status"] == "accepté"]["recommendation.produit_recommande"]
        .value_counts()
        .head(5)
        .to_dict()
    )

    # Retourner sous forme de dict
    return {
        "total_recommendations": total_recos,
        "clients_with_recommendations": clients_with_recos,
        "accepted": accepted,
        "refused": refused,
        "pending": pending,
        "top5_recommended": top5_recommended,
        "top5_accepted": top5_accepted,
    }
# Exemple d'utilisation

def resume_recommandations_client(client_id: str):
    """
    Retourne un résumé des recommandations pour un seul client :
    - Nombre de produits acceptés, refusés, en cours
    - Nombre total de recommandations pour ce client
    - Top 5 des produits recommandés
    - Top 5 des produits acceptés
    """
    df = load_data(get_mongo_collection())

    # Filtrer sur ce client
    client_df = df[df["client_ref"] == client_id]

    if client_df.empty:
        return {"message": f"Aucune recommandation trouvée pour le client {client_id}"}

    # Compter les statuts
    accepted = int((client_df["status"] == "accepted").sum())
    refused = int((client_df["status"] == "refused").sum())
    pending = int((client_df["status"] == "pending").sum())

    # Total des recommandations pour ce client
    total_recos = int(len(client_df))

    # Top 5 des produits recommandés
    top5_recommended = (
        client_df["recommendation.produit_recommande"]
        .value_counts()
        .head(5)
        .to_dict()
    )

    # Top 5 des produits acceptés
    top5_accepted = (
        client_df[client_df["status"] == "accepté"]["recommendation.produit_recommande"]
        .value_counts()
        .head(5)
        .to_dict()
    )
    # 
    from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv
import os


# --- 1. Connexion MongoDB ---
def get_mongo_collection():
    load_dotenv()
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client[os.getenv("MONGODB_DBNAME")]
    return db["client_recommendations"]


# --- 2. Charger les données ---
def load_data(collection):
    docs = list(collection.find({}))
    return pd.json_normalize(docs)


def resume_recommandations():
    """
    Retourne un résumé des recommandations :
    - Nombre de produits acceptés, refusés, en cours
    - Nombre total de recommandations
    - Nombre de clients avec au moins une recommandation
    - Top 5 des produits les plus recommandés
    - Top 5 des produits les plus acceptés
    """
    df = load_data(get_mongo_collection())

    # Compter les statuts (cast en int)
    accepted = int((df["status"] == "accepté").sum())
    refused = int((df["status"] == "refusé").sum())
    pending = int((df["status"] == "en cours").sum())

    # Total des recommandations
    total_recos = int(len(df))

    # Nombre de clients avec au moins une recommandation
    clients_with_recos = int(df["client_ref"].nunique())

    # Top 5 des produits recommandés (tous statuts confondus)
    top5_recommended = (
        df["recommendation.produit_recommande"]
        .value_counts()
        .head(5)
        .to_dict()
    )

    # Top 5 des produits acceptés
    top5_accepted = (
        df[df["status"] == "accepté"]["recommendation.produit_recommande"]
        .value_counts()
        .head(5)
        .to_dict()
    )

    # Retourner sous forme de dict
    return {
        "total_recommendations": total_recos,
        "clients_with_recommendations": clients_with_recos,
        "accepted": accepted,
        "refused": refused,
        "pending": pending,
        "top5_recommended": top5_recommended,
        "top5_accepted": top5_accepted,
    }
# Exemple d'utilisation

def resume_recommandations_client(client_id: str):
    """
    Retourne un résumé des recommandations pour un seul client :
    - Nombre de produits acceptés, refusés, en cours
    - Nombre total de recommandations pour ce client
    - Top 5 des produits recommandés
    - Top 5 des produits acceptés
    """
    df = load_data(get_mongo_collection())

    # Filtrer sur ce client
    client_df = df[df["client_ref"] == client_id]

    if client_df.empty:
        return {"message": f"Aucune recommandation trouvée pour le client {client_id}"}

    # Compter les statuts
    accepted = int((client_df["status"] == "accepted").sum())
    refused = int((client_df["status"] == "refused").sum())
    pending = int((client_df["status"] == "pending").sum())

    # Total des recommandations pour ce client
    total_recos = int(len(client_df))

    # Top 5 des produits recommandés
    top5_recommended = (
        client_df["recommendation.produit_recommande"]
        .value_counts()
        .head(5)
        .to_dict()
    )

    # Top 5 des produits acceptés
    top5_accepted = (
        client_df[client_df["status"] == "accepté"]["recommendation.produit_recommande"]
        .value_counts()
        .head(5)
        .to_dict()
    )
    recommandations_details = client_df[
        ["recommendation.produit_recommande", 
         "status", 
         "recommendation.raisonnement", 
         "recommendation.pitch"]
    ].to_dict(orient="records")
    
    # Retourner sous forme de dict
    return {
        "client_id": client_id,
        "total_recommendations": total_recos,
        "accepted": accepted,
        "refused": refused,
        "pending": pending,
        "top5_recommended": top5_recommended,
        "top5_accepted": top5_accepted,
        "recommendations_details": recommandations_details
    }
