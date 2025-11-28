# Fashion-Sense – Wardrobe AI (projet étudiant, travail en équipe)

Projet Django + React/Vite pour générer 3 looks classés par budget via une API DRF, avec génération d’images (HF/SD ou placeholder) et un front léger pour tester l’API.

## Équipe
- Sara Louise Sarah

## Architecture
- Backend : Django 5 / DRF, app `wardrobe`, endpoint `POST/GET /api/generate-look/`.
- Services IA : Mistral (texte) + Hugging Face router (images) + fallback placeholder inline.
- Frontend : React 18 + Vite (proxy `/api` → 127.0.0.1:8000).

## Prérequis
- Python 3.12+, Node 18+, npm.

## Installation backend
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Variables d’environnement (.env)
```ini
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# Texte (Mistral) : facultatif, fallback local si absent
MISTRAL_API_KEY=...
MISTRAL_MODEL=ministral-3b-latest
MISTRAL_API_URL=https://api.mistral.ai/v1/chat/completions

# Images Hugging Face (router) : optionnel, sinon fallback placeholder
HF_TOKEN=...
HF_IMAGE_MODEL=black-forest-labs/FLUX.1-schnell
HF_IMAGE_API=https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell


```

## API
- `POST /api/generate-look/` body `{"user_input": "tenue pour un mariage en été, budget moyen"}`  
  -> crée une `FashionRequest`, 3 `Look`, tente une image (HF > SD > placeholder data URL).
- `GET /api/generate-look/?limit=5` -> dernières requêtes avec leurs looks.

## Tests backend
```bash
.venv\Scripts\activate
python manage.py test wardrobe
```

## Frontend
```bash
cd frontend
npm install
npm run dev   # http://127.0.0.1:5173
```
Le proxy Vite envoie `/api` vers `http://127.0.0.1:8000`. Assure-toi que le backend tourne.

## Notes sur les images
- Si HF renvoie une erreur (400/404/410), le code passe automatiquement à SD puis à un placeholder inline (toujours une image affichable).
- Pour voir de vraies images, utiliser un endpoint HF actif (router) ou un backend SD valide, puis redémarrer le backend et générer de nouvelles requêtes (les anciennes entrées peuvent avoir `image_url` null).

## Commandes utiles
```bash
python manage.py shell -c "from wardrobe.models import FashionRequest; FashionRequest.objects.all().delete()"
```
Pour repartir sans ancien historique si besoin.
