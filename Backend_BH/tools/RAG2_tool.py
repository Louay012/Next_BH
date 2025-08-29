
import asyncio
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


class Query(BaseModel):
    question: str
    file_path: str

def get_or_create_vectorstore(file_path: str) -> FAISS:
    """Charge ou crée un vectorstore FAISS pour un fichier PDF
    
    """
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


async def chat(query: Query):
    try:
        if not Path(query.file_path).exists():
            raise Exception("Fichier introuvable")

        vectorstore = get_or_create_vectorstore(query.file_path)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        retrieved_docs = retriever.get_relevant_documents(query.question)

        # Fusionner les passages trouvés
        contenu = "\n\n".join(doc.page_content for doc in retrieved_docs)

        return {
            "question": query.question,
            "contenu_conditions_generales": contenu
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Initialisation de l'application 

from langchain_core.tools import tool
@tool
async def rag_tool(
        file_path: str        
):
    """Fonction principale pour exécuter l'outil RAG
    args:
        file_path (str): Chemin du fichier PDF à traiter depuis la liste_produits.
    """
    question: str = "Quel est le contenu de ce document ?"
    try:
        query = Query(question=question, file_path=file_path)
        #result = asyncio.run(chat(query))
        result = await chat(query)
        return result
        
    except Exception as e:
        raise Exception(detail=str(e))
    

#note cette fonction est asyncrone
# Exemple d'utilisation de rag_tool

"""print( asyncio.run(rag_tool(
    question="Quel est le contenu de ce document ?",
    file_path="d:/fezaimohamedelamine/StarterPack_sujet2/Conditions Générales/1-CG-Vie/CG_RAHMA.pdf"
)))"""