from rest_framework import serializers
from .models import FashionRequest, Look

class LookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Look
        fields = '__all__'

class FashionRequestSerializer(serializers.ModelSerializer):
    looks = LookSerializer(many=True, read_only=True)

    class Meta:
        model = FashionRequest
        fields = '__all__'
