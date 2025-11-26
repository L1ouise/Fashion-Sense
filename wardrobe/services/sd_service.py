import hashlib
import logging
import os
from typing import Optional

import requests

from .mistral_service import ServiceError

logger = logging.getLogger(__name__)


def generate_image(prompt: str) -> Optional[str]:
    """
    Generates an image URL using a text-to-image backend when configured.
    Falls back to a placeholder URL for local development.
    """

    api_key = os.getenv("SD_API_KEY")
    api_url = os.getenv("SD_API_URL")

    if not api_key or not api_url:
        digest = hashlib.md5(prompt.encode("utf-8")).hexdigest()[:6]
        return f"https://placehold.co/768x1024?text=Look+{digest}"

    payload = {"prompt": prompt, "num_inference_steps": 20}
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    response = requests.post(api_url, json=payload, headers=headers, timeout=60)

    if not response.ok:  # pragma: no cover - network bound
        logger.error("Stable Diffusion service returned %s", response.status_code)
        raise ServiceError("La génération d'image a échoué")

    data = response.json()
    return data.get("url") or data.get("image_url")
