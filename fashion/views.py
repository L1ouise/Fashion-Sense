from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FashionRequest
from .serializers import FashionRequestSerializer

class FashionRequestList(APIView):
    def get(self, request):
        queryset = FashionRequest.objects.all().order_by('-created_at')
        serializer = FashionRequestSerializer(queryset, many=True)
        return Response(serializer.data)

