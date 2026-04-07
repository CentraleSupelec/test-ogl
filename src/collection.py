import requests
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT: str = os.getenv("API_ENDPOINT", "https://ogl-api.ilaas.fr/api")
API_KEY: Optional[str] = os.getenv("API_KEY")

def create_collection(name: str, description: str, visibility: str, API_KEY: str  = None) -> str:
    """Créer une nouvelle collection via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data: Dict[str, Any] = {
        "name": name,
        "description": description,
        "visibility": visibility,
    }

    response = requests.post(f"{API_ENDPOINT}/v1/collections", json=data, headers=headers)

    if response.status_code == 201:
        return response.json().get("id", "")
    else:
        print(f"Error {response.status_code}: {response.text}")
        print("Request Data:", data)
        return f"Error: API request failed with status code {response.status_code}"
    
def get_me_infos(API_KEY: str = None) -> Any:
    """Obtenir les informations de l'utilisateur actuel via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{API_ENDPOINT}/v1/me/info", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
    

def delete_collection(collection_id: str, API_KEY: str  = None) -> str:
    """Supprimer une collection existante via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.delete(f"{API_ENDPOINT}/v1/collections/{collection_id}", headers=headers)

    if response.status_code == 204:
        return response.json().get("status", "No status returned")
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
    
def list_collections(API_KEY: str = None) -> Any:
    """Lister toutes les collections via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{API_ENDPOINT}/v1/collections", headers=headers)

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
    
def get_collection_details(collection_id: str, API_KEY: str  = None) -> Any:
    """Obtenir les détails d'une collection via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{API_ENDPOINT}/v1/collections/{collection_id}", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"

def patch_collection(collection_id: str, name: Optional[str] = None, description: Optional[str] = None, visibility: Optional[str] = None, API_KEY: str  = None) -> str:
    """Mettre à jour une collection existante via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data: Dict[str, Any] = {}
    if name:
        data["name"] = name
    if description:
        data["description"] = description
    if visibility:
        data["visibility"] = visibility

    response = requests.patch(f"{API_ENDPOINT}/v1/collections/{collection_id}", json=data, headers=headers)

    if response.status_code == 204:
        print(f"Collection {collection_id} updated successfully.")
        return "OK"
    else:
        print(f"Error {response.status_code}: {response.text}")
        print("Request Data:", data)
        return f"Error: API request failed with status code {response.status_code}"
