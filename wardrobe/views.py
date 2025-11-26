import logging
from typing import List

from rest_framework import generics, status
from rest_framework.response import Response

from .models import FashionRequest, Look
from .serializers import (
    FashionRequestSerializer,
    GenerateLookRequestSerializer,
    LookSerializer,
)
from .services import ServiceError, generate_image, generate_looks

logger = logging.getLogger(__name__)


def _load_history(limit: int = 5) -> List[str]:
    return list(
        FashionRequest.objects.order_by("-created_at").values_list("user_input", flat=True)[
            :limit
        ]
    )


class GenerateLookAPIView(generics.ListCreateAPIView):
    """
    Entrypoint: GET (liste des requêtes récentes) et POST /api/generate-look/
    """

    def get_serializer_class(self):
        return GenerateLookRequestSerializer if self.request.method == "POST" else FashionRequestSerializer

    def get_queryset(self):
        limit_param = self.request.query_params.get("limit", "5")
        try:
            limit = max(1, min(20, int(limit_param)))
        except ValueError:
            limit = 5

        return (
            FashionRequest.objects.order_by("-created_at")
            .prefetch_related("looks")
        )[:limit]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = FashionRequestSerializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            content_type="application/json; charset=utf-8",
        )

    def create(self, request, *args, **kwargs):
        payload = GenerateLookRequestSerializer(data=request.data)
        payload.is_valid(raise_exception=True)

        user_input = payload.validated_data["user_input"]
        history = _load_history()

        try:
            looks_payload = generate_looks(user_input=user_input, history=history)
        except ServiceError as exc:
            FashionRequest.objects.create(user_input=user_input, error_message=str(exc))
            return Response(
                {"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY
            )

        fashion_request = FashionRequest.objects.create(
            user_input=user_input, raw_response=looks_payload
        )

        look_instances = []
        sorted_payload = sorted(
            looks_payload, key=lambda l: l.get("budget_rank", 0) or 0
        )

        for index, look in enumerate(sorted_payload, start=1):
            prompt = (
                f"Tenue {index} inspirée de '{user_input}'. "
                f"Haut: {look.get('top', '')}. "
                f"Bas: {look.get('bottom', '')}. "
                f"Chaussures: {look.get('shoes', '')}. "
                f"Accessoires: {look.get('accessories', '')}. "
                "Style photo éditorial, lumière naturelle."
            )

            try:
                image_url = generate_image(prompt)
            except ServiceError as exc:
                logger.warning("Image generation failed for look %s: %s", index, exc)
                image_url = None

            look_instances.append(
                Look.objects.create(
                    fashion_request=fashion_request,
                    name=look.get("name", f"Look {index}"),
                    top=look.get("top", ""),
                    bottom=look.get("bottom", ""),
                    shoes=look.get("shoes", ""),
                    accessories=look.get("accessories", ""),
                    justification=look.get("justification", ""),
                    style_score=look.get("style_score", 4.0),
                    budget_rank=look.get("budget_rank", index),
                    budget_label=look.get("budget_label", "équilibré"),
                    image_url=image_url,
                    metadata={"prompt": prompt},
                )
            )

        response_data = FashionRequestSerializer(fashion_request).data
        response_data["looks"] = LookSerializer(look_instances, many=True).data
        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            content_type="application/json; charset=utf-8",
        )

# Create your views here.
