import base64
import hashlib
import logging
import os
from typing import Optional

import requests

from .mistral_service import ServiceError

logger = logging.getLogger(__name__)


def _placeholder(prompt: str) -> str:
    digest = hashlib.md5(prompt.encode("utf-8")).hexdigest()[:6]
    return f"https://placehold.co/768x1024?text=Look+{digest}"


def _generate_hf_image(prompt: str) -> Optional[str]:
    token = os.getenv("HF_TOKEN")
    model = os.getenv("HF_IMAGE_MODEL", "stabilityai/stable-diffusion-3.5-large")
    if not token:
        return None

    api_url = os.getenv("HF_IMAGE_API", "https://router.huggingface.co/v1/text-to-image")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"model": model, "prompt": prompt}

    response = requests.post(api_url, headers=headers, json=payload, timeout=60)
    if response.status_code != 200:  # pragma: no cover - network bound
        logger.warning("HF image generation failed (%s): %s", response.status_code, response.text)
        return None

    # HF router returns raw image bytes; encode as data URL so the frontend can display it directly.
    if not response.content:
        return None
    encoded = base64.b64encode(response.content).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def _generate_sd_image(prompt: str) -> Optional[str]:
    api_key = os.getenv("SD_API_KEY")
    api_url = os.getenv("SD_API_URL")
    if not api_key or not api_url:
        return None

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


def generate_image(prompt: str) -> Optional[str]:
    """
    Generates an image using (priority):
    1) Hugging Face inference API (HF_TOKEN + HF_IMAGE_MODEL),
    2) SD_API_URL + SD_API_KEY,
    otherwise returns a placeholder URL.
    """

    # Try HF first
    try:
        hf_url = _generate_hf_image(prompt)
        if hf_url:
            return hf_url
    except Exception as exc:  # pragma: no cover - network bound
        logger.warning("HF image generation error, falling back to SD/placeholder: %s", exc)

    # Then SD backend if configured
    try:
        sd_url = _generate_sd_image(prompt)
        if sd_url:
            return sd_url
    except ServiceError:
        raise
    except Exception as exc:  # pragma: no cover - network bound
        logger.warning("SD image generation error, falling back to placeholder: %s", exc)

    # Fallback placeholder
    return _placeholder(prompt)
