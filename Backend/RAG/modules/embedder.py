from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

def create_or_load_vectorstore(splits, index_path="embeddings/faiss_index"):
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Si l'index existe, on le charge
    if os.path.exists(index_path):
        return FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)
    else:
        # Sinon, on le crée à partir des documents "splits"
        vectorstore = FAISS.from_documents(splits, embedding)
        vectorstore.save_local(index_path)
        return vectorstore
