import requests
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT: str = os.getenv("API_ENDPOINT", "https://ogl-api.ilaas.fr/api")

def get_models(API_KEY: str = None) -> Any:
    """Lister les modèles disponibles via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{API_ENDPOINT}/v1/models", headers=headers)

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"

def get_model_details(model_id: str, API_KEY: str = None) -> Any:
    """Obtenir les détails d'un modèle via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{API_ENDPOINT}/v1/models/{model_id}", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"