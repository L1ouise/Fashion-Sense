from rest_framework import serializers

from .models import FashionRequest, Look


class GenerateLookRequestSerializer(serializers.Serializer):
    user_input = serializers.CharField(
        allow_blank=False,
        max_length=1000,
        help_text="Description libre de la tenue recherchée",
    )


class LookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Look
        fields = [
            "id",
            "name",
            "top",
            "bottom",
            "shoes",
            "accessories",
            "justification",
            "style_score",
            "budget_rank",
            "budget_label",
            "image_url",
            "created_at",
        ]


class FashionRequestSerializer(serializers.ModelSerializer):
    looks = LookSerializer(many=True, read_only=True)

    class Meta:
        model = FashionRequest
        fields = [
            "id",
            "user_input",
            "created_at",
            "looks",
        ]
