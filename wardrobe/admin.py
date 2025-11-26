from django.contrib import admin

from .models import FashionRequest, Look


@admin.register(FashionRequest)
class FashionRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "user_input", "created_at", "error_message")
    search_fields = ("user_input",)
    readonly_fields = ("created_at",)


@admin.register(Look)
class LookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "fashion_request",
        "budget_rank",
        "style_score",
        "created_at",
    )
    list_filter = ("budget_label",)
    search_fields = ("name", "justification")
    readonly_fields = ("created_at",)
