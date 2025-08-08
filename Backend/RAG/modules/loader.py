from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def load_all_pdfs_in_directory(root_dir):
    all_splits = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=20
    )

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(dirpath, filename)
                print(f"Chargement de : {pdf_path}")
                try:
                    loader = PyMuPDFLoader(pdf_path)
                    docs = loader.load()
                    splits = splitter.split_documents(docs)
                    all_splits.extend(splits)
                except Exception as e:
                    print(f"Erreur lors du chargement de {pdf_path} : {e}")
    
    return all_splits
