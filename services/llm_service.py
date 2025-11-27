from fashion.models import FashionRequest, Look

def generate_looks_for_request(fashion_request_id):
    """
    Génère automatiquement 3 Looks pour une FashionRequest.
    Simulation simple pour tester.
    """
    try:
        request = FashionRequest.objects.get(id=fashion_request_id)
    except FashionRequest.DoesNotExist:
        return "FashionRequest non trouvée"

    # Exemple de 3 Looks simulés
    looks_data = [
        {
            "title": "Look Casual",
            "haut": "T-shirt blanc",
            "bas": "Jean bleu",
            "chaussures": "Baskets blanches",
            "accessoires": "Montre",
            "justification": "Look simple et confortable",
            "prix_total": 70.0,
            "image_url": ""
        },
        {
            "title": "Look Chic",
            "haut": "Chemise en lin",
            "bas": "Chino beige",
            "chaussures": "Mocassins",
            "accessoires": "Ceinture en cuir",
            "justification": "Parfait pour un événement semi-formel",
            "prix_total": 150.0,
            "image_url": ""
        },
        {
            "title": "Look Estival",
            "haut": "Polo léger",
            "bas": "Short kaki",
            "chaussures": "Sandales",
            "accessoires": "Lunettes de soleil",
            "justification": "Look parfait pour un mariage d’été",
            "prix_total": 90.0,
            "image_url": ""
        },
    ]

    # Crée les Looks dans la base de données
    for look_data in looks_data:
        Look.objects.create(fashion_request=request, **look_data)

    return "Looks générés avec succès"
