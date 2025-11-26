from django.urls import path

from .views import GenerateLookAPIView

urlpatterns = [
    path("generate-look/", GenerateLookAPIView.as_view(), name="generate-look"),
]
