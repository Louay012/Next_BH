

from pydantic import BaseModel
import requests

class TranslationRequest(BaseModel):
    text: str

def translate(req: TranslationRequest):
    """
    Translate text from French to Arabic using LibreTranslate API.
    Args:
        req (TranslationRequest): Request containing the text to translate.
    """
    if not req.text.strip():
        return {"error": "Le texte est vide."}
    
    try:
        response = requests.post(
            "https://libretranslate.de/translate",
            json={
                "q": req.text,
                "source": "fr",
                "target": "ar",
                "format": "text"
            },
            headers={"accept": "application/json"},
            timeout=10
        )

        if response.status_code != 200:
            return {"error": f"HTTP {response.status_code}: {response.text}"}

        data = response.json()
        return {"translation": data.get("translatedText", "")}

    except Exception as e:
        return {"error": str(e)}