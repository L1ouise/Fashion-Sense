from django.db import models

class FashionRequest(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Requête #{self.id} - {self.description[:30]}..."

class Look(models.Model):
    fashion_request = models.ForeignKey(FashionRequest, on_delete=models.CASCADE, related_name="looks")
    
    title = models.CharField(max_length=200)
    haut = models.CharField(max_length=200)
    bas = models.CharField(max_length=200)
    chaussures = models.CharField(max_length=200)
    accessoires = models.TextField()
    justification = models.TextField()
    prix_total = models.FloatField(default=0.0)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Look {self.title} (req {self.fashion_request.id})"
