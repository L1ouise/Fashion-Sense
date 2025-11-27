from django.contrib import admin
from .models import FashionRequest, Look

@admin.register(FashionRequest)
class FashionRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "created_at")
    search_fields = ("description",)

@admin.register(Look)
class LookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "fashion_request", "prix_total")
    list_filter = ("fashion_request",)
    search_fields = ("title", "haut", "bas", "chaussures")
