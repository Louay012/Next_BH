# --------------------------
# modules/model.py
# --------------------------
from langchain.llms import CTransformers
from langchain_core.messages import SystemMessage

system_message = SystemMessage(content="Réponds toujours en français, même si la question est posée en anglais.")

def load_llm(model_path: str):
    """Charge le modèle LLM avec configuration"""
    llm = CTransformers(
        model=model_path,
        model_type="mistral",
        gpu_layers=10,
        config={
            "max_new_tokens": 200,
            "temperature": 0.3,
            "context_length": 2048
        }
    )
    return llm




