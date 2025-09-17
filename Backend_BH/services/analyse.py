from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv
import os
import numpy as np
from .detail_client import get_client_info

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


# --- 3. Résumé global des recommandations ---
def resume_recommandations():
    """
    Retourne un résumé des recommandations globales :
    - Nombre de produits acceptés, refusés, en cours
    - Nombre total de recommandations
    - Nombre de clients avec au moins une recommandation
    - Top 5 des produits les plus recommandés
    - Top 5 des produits les plus acceptés
    """
    df = load_data(get_mongo_collection())

    # Compter les statuts (cast en int natif)
    accepted = int((df["status"] == "accepted").sum())
    refused = int((df["status"] == "refused").sum())
    pending = int((df["status"] == "pending").sum())

    # Total des recommandations
    total_recos = int(len(df))

    # Nombre de clients avec au moins une recommandation
    clients_with_recos = int(df["client_ref"].nunique())

    # Top 5 des produits recommandés
    top5_recommended = (
        df["recommendation.produit_recommande"]
        .value_counts()
        .head(5)
        .astype(int)   # 🔥 conversion en int natif
        .to_dict()
    )

    # Top 5 des produits acceptés
    top5_accepted = (
        df[df["status"] == "accepté"]["recommendation.produit_recommande"]
        .value_counts()
        .head(5)
        .astype(int)   # 🔥 conversion en int natif
        .to_dict()
    )
        # Nombre de recommandations réalisées par jour
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        recos_par_jour = {
            str(k): v
            for k, v in (
                df.dropna(subset=["created_at"])
                .groupby(df["created_at"].dt.date)
                .size()
                .astype(int)
                .to_dict()
                .items()
            )
}
    else:
        recos_par_jour = {}


    return {
        "by_date": recos_par_jour,
        "total_recommendations": total_recos,
        "clients_with_recommendations": clients_with_recos,
        "accepted": accepted,
        "refused": refused,
        "pending": pending,
        "top5_recommended": top5_recommended,
        "top5_accepted": top5_accepted,
    }


# --- 4. Résumé des recommandations par client ---
def resume_recommandations_client(client_id: str):
    """
    Retourne un résumé des recommandations pour un seul client :
    - Nombre de produits acceptés, refusés, en cours
    - Nombre total de recommandations pour ce client
    - Top 5 des produits recommandés
    - Top 5 des produits acceptés
    - Détails des recommandations
    - Infos client
    """
    df = load_data(get_mongo_collection())

    # Filtrer sur ce client
    client_df = df[df["client_ref"] == client_id]
    client_info = get_client_info(client_id)

    if client_df.empty:
        return {"message": f"Aucune recommandation trouvée pour le client {client_id}"}

    # Compter les statuts (cast en int natif)
    accepted = int((client_df["status"] == "accepted").sum())
    refused = int((client_df["status"] == "refused").sum())
    pending = int((client_df["status"] == "pending").sum())

    # Total des recommandations
    total_recos = int(len(client_df))

    # Top 5 des produits recommandés
    top5_recommended = (
        client_df["recommendation.produit_recommande"]
        .value_counts()
        .head(5)
        .astype(int)   # 🔥 conversion en int natif
        .to_dict()
    )

    # Top 5 des produits acceptés
    top5_accepted = (
        client_df[client_df["status"] == "accepted"]["recommendation.produit_recommande"]
        .value_counts()
        .head(5)
        .astype(int)   # 🔥 conversion en int natif
        .to_dict()
    )

    # Détails des recommandations (nettoyage des NaN et int64)
    recommandations_details = (
        client_df[
            ["recommendation.produit_recommande",
             "status",
             "recommendation.raisonnement",
             "recommendation.score_pertinence",
             "recommendation.branche",
             "created_at",
             "recommendation.pitch"]
        ]
        .applymap(lambda x: None if pd.isna(x) else x)  # Replace NaN with None
        .applymap(lambda x: int(x) if isinstance(x, (np.int64, np.int32)) else x)  # Convert int64 to int
        .to_dict(orient="records")
    )

    return {
        "client_id": client_id,
        "total_recommendations": total_recos,
        "accepted": accepted,
        "refused": refused,
        "pending": pending,
        "top5_recommended": top5_recommended,
        "top5_accepted": top5_accepted,
        "recommendations_details": recommandations_details,
        "client_info": client_info
    }



def accepted_recommendations():
    """
    Retourne :
    - Le total des recommandations acceptées
    - La liste des recommandations acceptées triées par date (desc)
    """
    df = load_data(get_mongo_collection())

    # Vérifier la présence des colonnes
    required_cols = ["status", "client_ref", "recommendation.produit_recommande", "created_at"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Colonne manquante dans MongoDB : {col}")

    # Filtrer uniquement les 'accepted'
    df = df[df["status"] == "accepted"].copy()

    # Conversion des dates
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    # Trier par date DESC
    df = df.sort_values(by="created_at", ascending=False)

    # Construire la liste de résultats
    recos = df[["client_ref", "recommendation.produit_recommande", "created_at"]].to_dict(orient="records")

    return {
        "total_accepted": len(recos),
        "accepted_list": recos
    }

def refused_recommendations():
    """
    Retourne :
    - Le total des recommandations refusées
    - La liste des recommandations refusées triées par date (desc)
    """
    df = load_data(get_mongo_collection())

    # Vérifier la présence des colonnes
    required_cols = ["status", "client_ref", "recommendation.produit_recommande", "created_at"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Colonne manquante dans MongoDB : {col}")

    # Filtrer uniquement les 'refused'
    df = df[df["status"] == "refused"].copy()

    # Conversion des dates
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    # Trier par date DESC
    df = df.sort_values(by="created_at", ascending=False)

    # Construire la liste de résultats
    recos = df[["client_ref", "recommendation.produit_recommande", "created_at"]].to_dict(orient="records")

    return {
        "total_refused": len(recos),
        "refused_list": recos
    }


def pending_recommendations():
    df = load_data(get_mongo_collection())

    required_cols = ["status", "client_ref", "recommendation.produit_recommande", "created_at"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Colonne manquante dans MongoDB : {col}")

    df = df[df["status"] == "pending"].copy()
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    # Remplacer NaN par chaîne vide
    df["recommendation.produit_recommande"] = df["recommendation.produit_recommande"].fillna("")

    df = df.sort_values(by="created_at", ascending=False)

    recos = df[["client_ref", "recommendation.produit_recommande", "created_at"]].to_dict(orient="records")

    return {
        "total_pending": len(recos),
        "pending_list": recos
    }
