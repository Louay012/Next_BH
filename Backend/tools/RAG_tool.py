from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from ..RAG.modules.model import load_llm
from ..RAG.modules.rag_chain import create_rag_chain


class Query(BaseModel):
    question: str
    file_path: str

# Chargement initial du modèle
try:
    print(" Chargement du modèle LLM...")
    llm = load_llm("models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")
    print(" Modèle chargé avec succès.")
except Exception as e:
    print(f" Erreur lors du chargement du modèle: {e}")
    raise RuntimeError("Impossible de charger le modèle LLM")

# Fonctions utilitaires
def get_or_create_vectorstore(file_path: str) -> FAISS:
    """Charge ou crée un vectorstore FAISS pour un fichier PDF"""
    index_path = f"faiss_indexes/{Path(file_path).stem}"
    
    try:
        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    except Exception as e:
        raise RuntimeError(f"Erreur de chargement des embeddings: {e}")

    # Essai de chargement depuis le cache
    if Path(index_path).exists():
        try:
            return FAISS.load_local(
                index_path, 
                embedding, 
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            print(f" Erreur de chargement FAISS, reconstruction...: {e}")
            shutil.rmtree(index_path, ignore_errors=True)

    # Traitement du PDF
    try:
        loader = PyMuPDFLoader(file_path)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len
        )
        splits = text_splitter.split_documents(docs)
    except Exception as e:
        raise RuntimeError(f"Erreur de traitement du PDF: {e}")

    # Création et sauvegarde du vectorstore
    try:
        vectorstore = FAISS.from_documents(splits, embedding)
        vectorstore.save_local(index_path)
        return vectorstore
    except Exception as e:
        raise RuntimeError(f"Erreur de création du vectorstore: {e}")

# Endpoint principal
# In your main.py, update the chat endpoint like this:


#tool pour le système de questions-réponses
async def chat(query: Query):
    try:
        if not Path(query.file_path).exists():
            raise Exception("Fichier introuvable")

        vectorstore = get_or_create_vectorstore(query.file_path)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        
        rag_chain = create_rag_chain(llm, retriever)
        
        # Appel cohérent avec les clés définies
        result = rag_chain.invoke({"question": query.question})
        
        response = {
            "answer": result["result"],
            "sources": list(set(
                doc.metadata.get("source", "Inconnu") 
                for doc in result["source_documents"]
            ))
        }
        
        return JSONResponse(content=response)
        
    except Exception as e:
        raise Exception(detail=str(e))