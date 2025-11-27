import os
import json,re
import requests
from .history_service import get_user_history

HF_TOKEN = os.getenv("HF_TOKEN")
MISTRAL_MODEL = "google/gemma-2-2b-it"
API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def parse_model_output(output_text):
    """
    Supprime les backticks ```json ... ``` et retourne un JSON python.
    """
    cleaned = re.sub(r"```json|```", "", output_text).strip()
    return json.loads(cleaned)

def generate_fashion_looks(user_text):
    history = get_user_history()

    system_prompt = """
You are a professional fashion stylist AI.
Generate EXACTLY 3 complete outfits.
Return output STRICTLY in JSON format.
"""

    user_prompt = f"""
User request:
{user_text}

User fashion history:
{history}

Each outfit must contain:
- name (string)
- haut (string)
- bas (string)
- chaussures (string)
- accessoires (string)
- justification (string)
- budget (low/medium/high)
- score (float from 1 to 5)

Return ONLY a JSON list of 3 outfits.
"""

    payload = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    try:
        output_text = response.json()["choices"][0]["message"]["content"]
        return parse_model_output(output_text)
    except Exception as e:
        print("Parsing error:", e)
        print("Response:", response.text)
        return []