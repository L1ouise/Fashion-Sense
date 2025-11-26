import json
import logging
import os
import random
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class ServiceError(Exception):
    """Raised when an upstream AI service fails."""


def generate_looks(user_input: str, history: Optional[List[str]] = None) -> List[Dict]:
    """
    Calls an LLM (Mistral) to propose looks, falling back to deterministic
    suggestions when no API key is configured.
    """

    history = history or []
    api_key = os.getenv("MISTRAL_API_KEY")

    if api_key:
        try:
            return _call_mistral(user_input=user_input, history=history, api_key=api_key)
        except Exception as exc:  # pragma: no cover - network bound
            logger.exception("Mistral API failed, using fallback suggestions")
            raise ServiceError("Erreur lors de la génération des tenues via Mistral") from exc

    return _fallback_looks(user_input=user_input, history=history)


def _call_mistral(user_input: str, history: List[str], api_key: str) -> List[Dict]:
    model = os.getenv("MISTRAL_MODEL", "ministral-3b-latest")
    url = os.getenv("MISTRAL_API_URL", "https://api.mistral.ai/v1/chat/completions")

    history_text = " | ".join(history[-5:])
    messages = [
        {
            "role": "system",
            "content": (
                "Tu es un styliste professionnel. "
                "Retourne uniquement du JSON compact avec une clé 'looks' contenant une liste de 3 tenues. "
                "Chaque tenue doit inclure name, top, bottom, shoes, accessories, justification, "
                "style_score (note sur 5), budget_rank (1 à 3), budget_label. "
                "Classe les looks du plus accessible au plus premium. "
                "Inspire-toi de l'historique utilisateur pour affiner le style."
            ),
        },
        {
            "role": "user",
            "content": f"Historique: {history_text or 'aucun'}\nDemande: {user_input}",
        },
    ]

    payload = {
        "model": model,
        "messages": messages,
        "response_format": {"type": "json_object"},
        "temperature": 0.55,
        "max_tokens": 800,
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    parsed = json.loads(content)

    looks = parsed.get("looks") or parsed.get("tenues")
    if not looks or not isinstance(looks, list):
        raise ServiceError("Réponse inattendue de l'API Mistral")

    # Normalize keys to the expected format.
    normalized = []
    for index, look in enumerate(looks, start=1):
        normalized.append(
            {
                "name": look.get("name") or f"Look {index}",
                "top": look.get("top", ""),
                "bottom": look.get("bottom", ""),
                "shoes": look.get("shoes", ""),
                "accessories": look.get("accessories", ""),
                "justification": look.get("justification", ""),
                "style_score": float(look.get("style_score", 4)),
                "budget_rank": int(look.get("budget_rank", index)),
                "budget_label": look.get("budget_label", "equilibré"),
            }
        )
    normalized.sort(key=lambda l: l.get("budget_rank", 0))
    return normalized


def _fallback_looks(user_input: str, history: List[str]) -> List[Dict]:
    """
    Deterministic looks used for local/dev environments.
    """

    base_score = 4.0 + (random.random() * 0.6)  # slight variance for dev realism
    history_hint = history[-1] if history else ""
    theme = "élégant" if "mariage" in user_input.lower() else "casual chic"

    suggestions = [
        {
            "name": "Look 1 — Accessible",
            "top": "Chemise en lin écru respirante",
            "bottom": "Pantalon chino beige clair",
            "shoes": "Derbies en cuir souple camel",
            "accessories": "Ceinture tressée + montre minimaliste",
            "justification": (
                f"Base légère et polyvalente inspirée de '{history_hint}' pour rester {theme} "
                "avec un budget maîtrisé."
            ),
            "style_score": round(base_score, 1),
            "budget_rank": 1,
            "budget_label": "accessible",
        },
        {
            "name": "Look 2 — Équilibré",
            "top": "Blazer déstructuré bleu nuit + polo en maille",
            "bottom": "Pantalon ajusté gris perle",
            "shoes": "Mocassins en cuir grainé",
            "accessories": "Pochette ton sur ton, bracelet acier",
            "justification": (
                "Coupe affûtée et matières confortables, adapté aux photos et aux mouvements."
            ),
            "style_score": round(base_score + 0.2, 1),
            "budget_rank": 2,
            "budget_label": "équilibré",
        },
        {
            "name": "Look 3 — Signature",
            "top": "Veste croisée en laine froide + chemise popeline",
            "bottom": "Pantalon à pinces anthracite",
            "shoes": "Double boucles en cuir noir",
            "accessories": "Nœud papillon texturé, boutons de manchette sobres",
            "justification": (
                "Silhouette premium pour un rendu photo élégant et intemporel."
            ),
            "style_score": round(base_score + 0.4, 1),
            "budget_rank": 3,
            "budget_label": "premium",
        },
    ]
    return suggestions
