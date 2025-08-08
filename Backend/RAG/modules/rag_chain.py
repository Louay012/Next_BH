from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def create_rag_chain(llm, retriever):
    template = """Tu es un assistant expert en assurance.
Réponds toujours en français, même si la question est posée dans une autre langue.

Contexte:
{context}

Question:
{question}

Réponse (en français):
"""
    prompt = PromptTemplate(
        input_variables=["context", "question"],  # Changé de 'query' à 'question'
        template=template,
    )
    
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        input_key="question",  # Explicitement défini
        output_key="result",
        chain_type_kwargs={
            "prompt": prompt,  # Correction de la faute de frappe
            "verbose": True
        }
    )