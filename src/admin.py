import requests
from typing import Optional, Dict, Any, List
import os
from dotenv import load_dotenv
import json
load_dotenv()

API_ENDPOINT: str = os.getenv("API_ENDPOINT", "https://ogl-api.ilaas.fr/api")


def add_document_to_collection(
    collection: str, file: str, chunker: str = "RecursiveCharacterTextSplitter", 
    chunk_size: int = 2048, chunk_min_size: int = 0, chunk_overlap: int = 0, 
    length_function: str = "len", metadata: Dict = {}, output_format: str = "markdown",API_KEY: str  = None) -> str:
    
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
        "collection": collection,
        "limit": limit,
        "offset": offset,
    }

    response = requests.get(f"{API_ENDPOINT}/v1/documents", headers=headers, params=data)

    if response.status_code == 200:
        return response.json().get("documents", [])
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


def get_roles(API_KEY: str = None):
    """Obtenir les rôles disponibles via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{API_ENDPOINT}/v1/admin/roles", headers=headers)

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
    
# def create_tokens(user_id: int, name: str =1) -> Any:
#     """Créer des tokens d'API via l'API externe."""
#     if not API_KEY:
#         raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

#     headers: Dict[str, str] = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json",
#     }

#     data = {
#         "user": user_id,
#         "number_of_tokens": number_of_tokens,
#     }

#     response = requests.post(f"{API_ENDPOINT}/v1/admin/tokens", headers=headers, json=data)

#     if response.status_code == 201:
#         return response.json().get("data", [])
#     else:
#         print(f"Error {response.status_code}: {response.text}")
#         return f"Error: API request failed with status code {response.status_code}"

def patch_role(
    role_id: int,
    name: Optional[str] = None,
    permissions: Optional[List[str]] = None,
    limits: Optional[List[Dict[str, Any]]] = None,
    API_KEY: str  = None
) -> str:
    """Mettre à jour un rôle existant via l'API externe (PATCH /roles/{role})."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data: Dict[str, Any] = {}

    # Champs optionnels, on n'envoie que ceux qui sont fournis
    if name is not None:
        data["name"] = "Test2"

    if permissions is not None:
        data["permissions"] = permissions

    if limits:
        data["limits"] = limits

    if not data:
        raise ValueError("Aucune donnée à mettre à jour (name/permissions/limits).")

    # Exemple d'appel (à adapter à ta stack : requests/httpx et ton endpoint)
    resp = requests.patch(f"{API_ENDPOINT}/v1/admin/roles/{role_id}", headers=headers, json=data, timeout=30)
    if resp.status_code == 204:
        print("Role updated successfully.")
        return "OK"
    if resp.status_code == 422:
        print(f"Validation error: {resp.text}")
        return f"Validation error: {resp.text}"
    resp.raise_for_status()
    return resp.text

def create_role(
    name: str,
    permissions: Optional[List[str]] = None,
    limits: Optional[List[Dict[str, Any]]] = None,
    API_KEY: str  = None
) -> Any:
    """Créer un nouveau rôle via l'API externe."""
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
    }
    if permissions is not None:
        data["permissions"] = permissions
    if limits is not None:
        data["limits"] = limits
    response = requests.post(f"{API_ENDPOINT}/v1/admin/roles", headers=headers, json=data)
    if response.status_code == 201:
        print(response.json())
        return response.json().get("id", {})
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"

def create_user(email,name,password,role,organization= 0,budget=0,expires= 0,priority= 0, API_KEY: str  = None) -> Any:
    """Créer un nouvel utilisateur via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data: Dict[str, Any] = {
        "email": email,
        "name": name,
        "password": password,
        "role": role,
        "budget": budget,
        "expires": expires,
        "priority": priority,
    }
    response = requests.post(f"{API_ENDPOINT}/v1/admin/users", headers=headers, json=data)
    if response.status_code == 201:
        return response.json().get("id", {})
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"

def get_users(role_id: Optional[int] = None, API_KEY: str  = None) -> Any:
    """Obtenir les utilisateurs via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {}
    if role_id is not None:
        data["role"] = role_id
    response = requests.get(f"{API_ENDPOINT}/v1/admin/users", headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
    
def create_token(user_id: int, name: str = "default", expires = 1767049200, API_KEY: str  = None) -> Any:
    """Créer un token d'API via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")


    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "user": user_id,
        "name": name,
        "expires": expires,
    }

    response = requests.post(f"{API_ENDPOINT}/v1/admin/tokens", headers=headers, json=data)

    if response.status_code == 201:
        return response.json().get("token", ""), response.json().get("id", "")
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"

def get_tokens_by_user(user_id: int, API_KEY: str  = None) -> Any:
    """Obtenir les tokens d'un utilisateur via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "user": user_id,
    }
    response = requests.get(f"{API_ENDPOINT}/v1/admin/tokens", headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"

def get_tokens(token_id: int, API_KEY: str  = None) -> Any:
    """Obtenir les détails d'un token d'API via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{API_ENDPOINT}/v1/admin/tokens/{token_id}", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"


def get_routers(API_KEY: str = None):
    """Obtenir les routeurs disponibles via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{API_ENDPOINT}/v1/admin/routers", headers=headers)

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
    
def get_providers(router_id: int, offset: int = 0, limit: int = 10, order_by: str = "id", order_direction: str = "asc", API_KEY: str  = None) -> Any:
    """Obtenir les fournisseurs disponibles via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "router": router_id,
        "offset": offset,
        "limit": limit,
        "order_by": order_by,
        "order_direction": order_direction,
    }
    response = requests.get(f"{API_ENDPOINT}/v1/admin/providers", headers=headers)

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
    
def update_user(
    user_id: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    current_password: Optional[str] = None,
    password: Optional[str] = None,
    role: Optional[int] = None,
    organization: Optional[int] = None,
    budget: Optional[float] = None,
    expires: Optional[int] = None,
    priority: Optional[int] = None,
    API_KEY: str  = None
) -> str:
    """Mettre à jour un utilisateur existant via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data: Dict[str, Any] = {}

    if name is not None:
        data["name"] = name
    if email is not None:
        data["email"] = email
    if password is not None:
        data["password"] = password
    if role is not None:
        data["role"] = role
    if organization is not None:
        data["organization"] = organization
    if budget is not None:
        data["budget"] = budget
    if expires is not None:
        data["expires"] = expires
    if priority is not None:
        data["priority"] = priority

    if not data:
        raise ValueError("Aucune donnée à mettre à jour.")

    response = requests.patch(f"{API_ENDPOINT}/v1/admin/users/{user_id}", headers=headers, json=data)

    if response.status_code == 204:
        return "OK"
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
    
def delete_user(user_id: int, API_KEY: str  = None) -> str:
    """Supprimer un utilisateur existant via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.delete(f"{API_ENDPOINT}/v1/admin/users/{user_id}", headers=headers)

    if response.status_code == 204:
        return "OK"
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
    
def delete_token(token_id: int, API_KEY: str  = None) -> str:
    """Supprimer un token d'API existant via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.delete(f"{API_ENDPOINT}/v1/admin/tokens/{token_id}", headers=headers)

    if response.status_code == 204:
        return "OK"
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"

def delete_role(role_id: int, API_KEY: str  = None) -> str:
    """Supprimer un rôle existant via l'API externe."""
    if not API_KEY:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("La clé API n'a pas été trouvée. Vérifiez vos configurations.")
        
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.delete(f"{API_ENDPOINT}/v1/admin/roles/{role_id}", headers=headers)

    if response.status_code == 204:
        return "OK"
    else:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: API request failed with status code {response.status_code}"
