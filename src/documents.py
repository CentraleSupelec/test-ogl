import requests
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv
import json
load_dotenv()

API_ENDPOINT: str = os.getenv("API_ENDPOINT", "https://ogl-api.ilaas.fr/api")


def add_document_to_collection(
    collection: str, file: str, chunker: str = "RecursiveCharacterTextSplitter", 
    chunk_size: int = 512, chunk_min_size: int = 0, chunk_overlap: int = 0, 
    length_function: str = "len", metadata: Dict = {}, output_format: str = "markdown", API_KEY: str  = None) -> str:
    
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
    }

    # Déterminer le type MIME en fonction de l'extension
    file_extension = os.path.splitext(file)[1].lower()
    mime_types = {
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.txt': 'text/plain',
        '.csv': 'text/csv',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.xls': 'application/vnd.ms-excel',
    }
    
    mime_type = mime_types.get(file_extension, 'application/octet-stream')

    with open(file, "rb") as f:
        files = {
            "file": (os.path.basename(file), f, mime_type),
        }

        data = {
            "collection": str(collection),
            "output_format": output_format,
            "chunker": chunker,
            "chunk_size": str(chunk_size),  # Convertir en string
            "chunk_min_size": str(chunk_min_size),
            "chunk_overlap": str(chunk_overlap),
            "length_function": length_function,
            "metadata": json.dumps(metadata),
        }

        response = requests.post(
            f"{API_ENDPOINT}/v1/documents",
            headers=headers,
            files=files,
            data=data,
        )

    print("Status:", response.status_code)
    print("Raw response:", response.text)

    if response.status_code in (200, 201):
        try:
            return response.json().get("status", "No status field")
        except Exception:
            return "Document ajouté (réponse non JSON)"
    else:
        print("Request Data (form):", data)
        return f"Error: API request failed with status code {response.status_code}"


def get_documents_collection(collection: str, limit: int = 10, offset: int = 0, API_KEY: str  = None) -> Any:
    """Obtenir les documents d'une collection via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")
    
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "collection_id": collection,
        "limit": limit,
        "offset": offset,
    }

    response = requests.get(f"{API_ENDPOINT}/v1/documents", headers=headers, params=data)

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"


def get_document(document_id: str, API_KEY: str  = None) -> Any:
    """Obtenir les détails d'un document via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{API_ENDPOINT}/v1/documents/{document_id}", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"


def delete_document(document_id: str, API_KEY: str  = None) -> str:
    """Supprimer un document existant via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.delete(f"{API_ENDPOINT}/v1/documents/{document_id}", headers=headers)

    if response.status_code == 204:
        return response.json().get("status", "No status returned")
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
    

def get_chunks_document(document_id: str, limit: int = 10, offset: int = 0, API_KEY: str  = None) -> Any:
    """Obtenir les chunks d'un document via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")
    
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "limit": limit,
        "offset": offset,
        "document_id": document_id
    }

    response = requests.get(f"{API_ENDPOINT}/v1/documents/{document_id}/chunks", headers=headers, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
    
def get_chunk(chunk_id: int, document_id: int, API_KEY: str  = None) -> Any:
    """Obtenir les détails d'un chunk via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{API_ENDPOINT}/v1/documents/{document_id}/chunks/{chunk_id}", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
    
def delete_chunk(chunk_id: int, document_id: int, API_KEY: str  = None) -> str:
    """Supprimer un chunk existant via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.delete(f"{API_ENDPOINT}/v1/documents/{document_id}/chunks/{chunk_id}", headers=headers)

    if response.status_code == 204:
        return response.json().get("status", "No status returned")
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
    
