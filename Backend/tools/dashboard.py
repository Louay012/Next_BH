from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from collections import Counter
from datetime import datetime
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME")

app = FastAPI()

def get_db():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DBNAME]
    return db

@app.get("/api/recommendation-stats")
def recommendation_stats():
    db = get_db()
    col = db["client_recommendations"]
    data = list(col.find({}))
    total = len(data)
    status_counts = Counter([d.get("status", "unknown") for d in data])
    product_counts = Counter([d.get("recommendation", {}).get("produit_recommande", "unknown") for d in data])
    purchased = sum(1 for d in data if d.get("status") == "purchased")
    refused = sum(1 for d in data if d.get("status") == "refused")
    accepted = sum(1 for d in data if d.get("status") == "accepted")
    by_date = Counter([str(d.get("created_at", "")).split(" ")[0] for d in data if d.get("created_at")])

    return {
        "total_recommendations": total,
        "status_counts": status_counts,
        "product_counts": product_counts,
        "purchased": purchased,
        "refused": refused,
        "accepted": accepted,
        "by_date": by_date,
    }