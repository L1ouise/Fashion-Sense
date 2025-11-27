from django.db import models

class FashionRequest(models.Model):
    user_input = models.TextField(help_text="Texte saisi par l'utilisateur (ex: 'tenu mariage été, budget moyen')")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Request #{self.pk} - {self.user_input[:50]}"
    
class Look(models.Model):
    Budget_choices = [
        ('low', 'Budget faible'),
        ('medium', 'Budget moyen'),
        ('high', 'Budget élevé'),
    ]
    request = models.ForeignKey(FashionRequest, on_delete=models.CASCADE, related_name="looks")
    name = models.CharField(max_length=150, blank=True, help_text="Nom du look (ex: 'Élégance classique')")
    haut = models.CharField(max_length=255, blank=True)
    bas = models.CharField(max_length=255, blank=True)
    chaussures = models.CharField(max_length=255, blank=True)
    accessoires = models.CharField(max_length=255, blank=True)
    justification = models.TextField(blank=True)
    budget = models.CharField(max_length=10, choices=Budget_choices, default="medium")
    score = models.FloatField(null=True, blank=True, help_text="Score stylistique (ex: 4.5)")
    # image_url pour un lien absolu, image_file si tu veux stocker le fichier localement
    image_url = models.URLField(max_length=500, blank=True, null=True)
    image_file = models.ImageField(upload_to="outfits/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Look #{self.pk} ({self.budget}) for Request #{self.request_id}"
# Create your models here.
