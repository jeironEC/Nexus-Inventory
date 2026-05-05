from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from drf_spectacular.utils import extend_schema

from api.serializers.empty import EmptySerializer


@extend_schema(tags=["Health"])
class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes: list[str] = []
    serializer_class = EmptySerializer

    def get(self, request):
        return Response(
            {
                "status": "ok",
                "version": "1.0.0",
                "timestamp": timezone.now().date().isoformat(),
            }
        )
