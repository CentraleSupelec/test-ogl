import requests
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT: str = os.getenv("API_ENDPOINT", "https://ogl-api.ilaas.fr/api")

def embed_text(text: str, API_KEY: str = None, model: str = "default") -> Any:
    """Obtenir l'embedding d'un texte via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data: Dict[str, Any] = {
        "input": text,
        "model": model,
    }

    response = requests.post(f"{API_ENDPOINT}/v1/embeddings", json=data, headers=headers)

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"

def search_collection(collection: list, query: str, rff_k: int = 20,limit: int = 10, method: str = "semantic",score_threshold: float = 0.00,web_search: bool = False, web_search_k: int = 5, API_KEY: str  = None) -> Any:
    """Rechercher dans une collection via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "collections": collection,
        "prompt": query,
        # "rff_k": rff_k,
        # "limit":limit,
        "method": method,
        "score_threshold": score_threshold,
        # "web_search": web_search,
        # "web_search_k": web_search_k,
    }

    response = requests.post(f"{API_ENDPOINT}/v1/search", headers=headers, json=data)

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
