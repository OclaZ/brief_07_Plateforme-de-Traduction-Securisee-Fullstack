from fastapi import APIRouter, HTTPException, status, Depends
import os
import httpx
from typing import List, Dict, Any
from core.security import verify_token
from schemas.schemas import TranslateRequest, TranslateResponse, ErrorResponse
from dotenv import load_dotenv

load_dotenv()


router = APIRouter(tags=["translate"])



API_URL_en_fr = "https://router.huggingface.co/hf-inference/models/Helsinki-NLP/opus-mt-en-fr"
API_URL_fr_en = "https://router.huggingface.co/hf-inference/models/Helsinki-NLP/opus-mt-fr-en"
HUGGINGFACE_API_KEY = os.getenv("HF_TOKEN")
TIMEOUT = 30.0 


def validate_api_key() -> str:
    if not HUGGINGFACE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Clé API Hugging Face non configurée. Veuillez configurer HF_TOKEN dans le fichier .env"
        )
    return HUGGINGFACE_API_KEY


def query_huggingface(text: str, direction: str) -> List[List[Dict[str, Any]]]:
    # Validation de la clé API
    api_key = validate_api_key()

    if direction == "en_fr":
        api_url = API_URL_en_fr
    elif direction == "fr_en":
        api_url = API_URL_fr_en
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid direction. Allowed values: 'en_fr', 'fr_en'."
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {"inputs": text}

    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            response = client.post(api_url, headers=headers, json=payload)

            # Gestion des différents codes d'erreur HTTP
            if response.status_code == 401:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Clé API Hugging Face invalide ou expirée"
                )
            elif response.status_code == 429:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Limite de requêtes API Hugging Face atteinte. Veuillez réessayer plus tard"
                )
            elif response.status_code == 503:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Le modèle Hugging Face est en cours de chargement. Veuillez réessayer dans quelques instants"
                )
            elif response.status_code >= 500:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Erreur serveur Hugging Face (code {response.status_code})"
                )

            # Lever une exception pour les autres codes d'erreur
            response.raise_for_status()

            # Vérifier que la réponse est valide
            result = response.json()
            if not isinstance(result, list):
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Réponse invalide de l'API Hugging Face"
                )

            return result

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Timeout lors de l'appel à l'API Hugging Face (>{TIMEOUT}s)"
        )
    except httpx.NetworkError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erreur réseau lors de l'appel à l'API Hugging Face: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erreur HTTP {e.response.status_code} de l'API Hugging Face"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erreur inattendue lors de l'appel à l'API Hugging Face: {str(e)}"
        )


@router.post(
    "/translate",
    response_model=TranslateResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Requête invalide"},
        401: {"model": ErrorResponse, "description": "Token invalide ou expiré"},
        500: {"model": ErrorResponse, "description": "Clé API Hugging Face non configurée"},
        503: {"model": ErrorResponse, "description": "Service Hugging Face non disponible"},
        504: {"model": ErrorResponse, "description": "Timeout lors de l'appel à l'API Hugging Face"}
    },
    summary="Traduction de texte",
    description="Traduit un texte en utilisant l'API Hugging Face Inference (authentification requise)"
)
def translate(request: TranslateRequest, token_data: dict = Depends(verify_token)):
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le texte ne peut pas être vide"
        )

    # Appel à l'API Hugging Face
    translate = query_huggingface(request.text , request.direction)

    return TranslateResponse(
        text=request.text,
        traduction=translate
    )
