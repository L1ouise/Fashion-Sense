import os
import io
import base64
from django.conf import settings
from huggingface_hub import InferenceClient
from PIL import Image

# Initialisation du client HF
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(api_key=HF_TOKEN, provider="nscale")

SDXL_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"


def generate_outfit_image(prompt: str, filename: str = "outfit.png", return_base64: bool = True):
    """
    Génère une image d'un look via Stable Diffusion XL (HF InferenceClient).
    
    Args:
        prompt (str): description du look
        filename (str): nom du fichier à sauvegarder dans MEDIA_ROOT/outfits/
        return_base64 (bool): True pour base64, False pour URL MEDIA
    
    Returns:
        str | None: base64 ou URL MEDIA, None si erreur
    """
    try:
        # Génération image PIL
        image: Image.Image = client.text_to_image(prompt, model=SDXL_MODEL)

        # Créer dossier si nécessaire
        save_dir = os.path.join(settings.MEDIA_ROOT, "outfits")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)

        # Sauvegarder l'image sur disque
        image.save(save_path, format="PNG")

        if return_base64:
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            return base64.b64encode(img_bytes).decode("utf-8")
        else:
            return f"{settings.MEDIA_URL}outfits/{filename}"

    except Exception as e:
        print("❌ SDXL Error:", e)
        return None
