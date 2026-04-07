import requests
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT: str = os.getenv("API_ENDPOINT", "https://ogl-api.ilaas.fr/api")

def rerank_results(documents: list, query: str, model: str, top_n : int = 1, API_KEY: str  = None) -> Any:
    """Reranker les résultats d'une recherche via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "documents": documents,
        "query": query,
        "model": model,
        "top_n": top_n,
    }

    response = requests.post(f"{API_ENDPOINT}/v1/rerank", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
