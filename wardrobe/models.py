from django.db import models


class FashionRequest(models.Model):
    """
    Represents a single user request for outfits.
    """

    user_input = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    raw_response = models.JSONField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"Fashion request {self.pk}"


class Look(models.Model):
    """
    Stores each generated look attached to a FashionRequest.
    """

    fashion_request = models.ForeignKey(
        FashionRequest, related_name="looks", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    top = models.TextField()
    bottom = models.TextField()
    shoes = models.TextField()
    accessories = models.TextField()
    justification = models.TextField()
    style_score = models.DecimalField(max_digits=3, decimal_places=1)
    budget_rank = models.PositiveIntegerField(
        help_text="1 = le plus accessible, 3 = le plus premium"
    )
    budget_label = models.CharField(max_length=50, default="equilibré")
    image_url = models.URLField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["budget_rank", "created_at"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.name} (req {self.fashion_request_id})"
