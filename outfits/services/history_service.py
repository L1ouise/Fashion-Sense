from outfits.models import FashionRequest

def get_user_history(limit=3):
    requests = FashionRequest.objects.order_by("-created_at")[:limit]

    if not requests:
        return "No previous fashion history available."

    history_text = "Here is the user's recent fashion preferences:\n\n"
    for req in requests:
        history_text += f"- Request: {req.user_input}\n"
        for look in req.looks.all():
            history_text += f"  • Look: {look.haut}, {look.bas}, {look.chaussures} (Budget: {look.budget})\n"

    return history_text