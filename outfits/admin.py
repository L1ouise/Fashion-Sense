from django.contrib import admin
from .models import FashionRequest, Look

class LookInline(admin.TabularInline):
    model = Look
    extra = 0
    readonly_fields = ('created_at',)
@admin.register(FashionRequest)
class FashionRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_input', 'created_at')
    search_fields = ('user_input',)
    inlines = [LookInline]
@admin.register(Look)
class LookAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'name', 'budget', 'score', 'created_at')
    list_filter = ('budget', 'created_at')
    search_fields = ('name', 'haut', 'bas', 'chaussures', 'accessoires')
# Register your models here.
