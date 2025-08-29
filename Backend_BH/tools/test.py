from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os
from collections import Counter

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME", "next_bh")

app = FastAPI(title="NEXT_BH Client API")

# --- STATIC FALLBACK SAMPLE (matches Client.jsx staticData) ---
STATIC_SAMPLE = {
  "client_ref": "1381",
  "client_name": "Jean Dupont",
  "client_details": {
    "age": 63,
    "profession": "Chauffeur",
    "marital_status": "Marié",
    "contracts": ["Automobile", "Décès temporaire (expiré)"]
  },
  "recommendations": [
    {
      "id": "68a04264bd9cde4606fd0d47",
      "client_ref": "1381",
      "produit_recommande": "CG ASSURANCE GROUPE MALADIE",
      "branche": "Assurance Santé",
      "score_pertinence": "85/100",
      "score_value": 85,
      "created_at": "2025-08-16T10:33:40.982Z",
      "status": "Accepté",
      "raisonnement": "Le client est un chauffeur de 63 ans...",
      "pitch": "Cher Monsieur, ..."
    },
    {
      "id": "68a078bee1e32ce70fe983aa",
      "client_ref": "1381",
      "produit_recommande": "Assurance santé adaptée aux déplacements fréquents",
      "branche": "Santé",
      "score_pertinence": "90/100",
      "score_value": 90,
      "created_at": "2025-08-16T14:25:34.972Z",
      "status": "Refusé",
      "raisonnement": "Le client est un chauffeur de 63 ans...",
      "pitch": "Bonjour Jean Dupont, ..."
    }
  ],
  "stats": {
    "total_recommendations": 2,
    "accepted_count": 1,
    "refused_count": 1,
    "pending_count": 0,
    "avg_score": 87.5,
    "branch_distribution": {"Assurance Santé": 2},
    "score_distribution": {"81-100": 2},
    "timeline_data": [{"date": "2025-08-16", "count": 2}]
  }
}

# --- DB helper ---
def get_db():
    if not MONGODB_URI:
        return None
    client = MongoClient(MONGODB_URI)
    return client[MONGODB_DBNAME]

def _doc_to_dict(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc
    doc = dict(doc)
    doc["id"] = str(doc.get("_id", doc.get("id", "")))
    doc.pop("_id", None)
    # convert datetimes to isoformat
    for k in ("created_at", "updated_at"):
        if k in doc and isinstance(doc[k], datetime):
            doc[k] = doc[k].isoformat()
    return doc

# --- Pydantic model for status update ---
class StatusUpdate(BaseModel):
    status: str

# --- Aggregation util ---
def aggregate_recommendations(recs: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(recs)
    statuses = [r.get("status", "").lower() for r in recs]
    accepted = sum(1 for s in statuses if "accept" in s or s == "accepté" or s == "accepted")
    refused = sum(1 for s in statuses if "refus" in s or s == "refusé" or s == "refused")
    pending = total - accepted - refused
    scores = [r.get("score_value") for r in recs if isinstance(r.get("score_value"), (int, float))]
    avg_score = round(sum(scores) / len(scores), 1) if scores else None
    branch = Counter([r.get("branche", "Unknown") for r in recs])
    timeline = Counter([str(r.get("created_at", "")).split("T")[0] for r in recs if r.get("created_at")])
    # score buckets
    buckets = Counter()
    for s in scores:
        if s <= 20: buckets["0-20"] += 1
        elif s <= 40: buckets["21-40"] += 1
        elif s <= 60: buckets["41-60"] += 1
        elif s <= 80: buckets["61-80"] += 1
        else: buckets["81-100"] += 1
    return {
        "total_recommendations": total,
        "accepted_count": accepted,
        "refused_count": refused,
        "pending_count": pending,
        "avg_score": avg_score,
        "branch_distribution": dict(branch),
        "score_distribution": dict(buckets),
        "timeline_data": [{"date": d, "count": c} for d, c in sorted(timeline.items())]
    }

# --- Endpoints ---

@app.get("/api/client/{client_ref}")
def get_client(client_ref: str):
    """
    Return client object with recommendations and aggregated stats.
    Falls back to STATIC_SAMPLE when DB unavailable or no data.
    """
    db = get_db()
    if db:
        col = db.get("client_recommendations")
        docs = list(col.find({"client_ref": str(client_ref)}))
        if docs:
            recs = []
            for d in docs:
                rd = _doc_to_dict(d)
                # keep created_at as ISO if stored as datetime
                if isinstance(rd.get("created_at"), datetime):
                    rd["created_at"] = rd["created_at"].isoformat()
                recs.append(rd)
            stats = aggregate_recommendations(recs)
            result = {
                "client_ref": client_ref,
                "client_name": None,
                "client_details": {},
                "recommendations": recs,
                "stats": stats
            }
            return jsonable_encoder(result)
    # fallback static
    if STATIC_SAMPLE["client_ref"] == str(client_ref):
        return jsonable_encoder(STATIC_SAMPLE)
    # return sample if client not found
    sample = dict(STATIC_SAMPLE)
    sample["client_ref"] = client_ref
    return jsonable_encoder(sample)

@app.get("/api/recommendations")
def list_recommendations(client_ref: Optional[str] = None, limit: int = 100):
    """
    List recommendations. If client_ref provided, filter by it.
    Falls back to static sample when DB unavailable.
    """
    db = get_db()
    if db:
        col = db.get("client_recommendations")
        q = {}
        if client_ref:
            q["client_ref"] = str(client_ref)
        docs = list(col.find(q).limit(limit))
        return jsonable_encoder([_doc_to_dict(d) for d in docs])
    # fallback
    if client_ref and STATIC_SAMPLE["client_ref"] != str(client_ref):
        return []
    return jsonable_encoder(STATIC_SAMPLE["recommendations"])

@app.patch("/api/recommendation/{rec_id}/status")
def update_recommendation_status(rec_id: str, payload: StatusUpdate):
    """
    Update status of a recommendation by its _id (or id).
    If DB not configured, return 404.
    """
    db = get_db()
    if not db:
        raise HTTPException(status_code=503, detail="Database not configured (use MONGODB_URI in .env)")
    col = db.get("client_recommendations")
    # try ObjectId
    query = {"_id": ObjectId(rec_id)} if ObjectId.is_valid(rec_id) else {"id": rec_id}
    res = col.find_one_and_update(query, {"$set": {"status": payload.status, "updated_at": datetime.utcnow()}}, return_document=True)
    if not res:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return jsonable_encoder(_doc_to_dict(res))

@app.post("/api/recommendation")
def create_recommendation(doc: Dict[str, Any]):
    """
    Create a recommendation document (DB) or return sample created object when DB absent.
    """
    db = get_db()
    doc = dict(doc)
    doc.setdefault("created_at", datetime.utcnow())
    doc.setdefault("updated_at", datetime.utcnow())
    if db:
        col = db.get("client_recommendations")
        inserted = col.insert_one(doc)
        doc["_id"] = inserted.inserted_id
        return jsonable_encoder(_doc_to_dict(doc))
    # fallback: echo back with random id
    doc["id"] = f"local-{int(datetime.utcnow().timestamp())}"
    return jsonable_encoder(doc)

# Simple health endpoint
@app.get("/api/health")
def health():
    return {"status": "ok", "db_configured": bool(MONGODB_URI)}