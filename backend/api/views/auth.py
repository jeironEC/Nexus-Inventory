from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from nexus_inventory_backend.db.models import User

from api.serializers.password_reset import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from api.serializers.token_pair import EmailTokenObtainPairSerializer


class EmailTokenObtainPairViewSet(TokenObtainPairView):
    """
    Autenticación mediante email y contraseña.
    Retorna un par de tokens JWT (access y refresh).
    """

    serializer_class = EmailTokenObtainPairSerializer


class PasswordResetViewSet(viewsets.ViewSet):
    """
    Recuperación de contraseña mediante email.
    Si el email existe y es de un admin, permite realizar el cambio de contraseña
    """

    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "request":
            return PasswordResetRequestSerializer
        elif self.action == "confirm":
            return PasswordResetConfirmSerializer
        return None

    @action(detail=False, methods=["post"])
    def request(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "No se encontró un administrador con ese correo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.role.name.lower() != "admin":
            return Response(
                {"detail": "Only administrators are allowed this action."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Email validate."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def confirm(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        new_password = serializer.validated_data["new_password"]

        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"detail": "Invalid user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"detail": "Password updated successfully"},
            status=status.HTTP_200_OK,
        )
