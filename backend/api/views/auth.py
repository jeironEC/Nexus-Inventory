import uuid
from hashlib import sha256

from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from nexus_inventory_backend.db.models import User, PasswordResetOTP

from api.serializers.password_reset import (
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
    PasswordResetConfirmSerializer,
)
from api.serializers.token_pair import EmailTokenObtainPairSerializer
from api.services.email_service import send_reset_password_email
from api.services.util_service import generate_otp
from datetime import timedelta


class EmailTokenObtainPairViewSet(TokenObtainPairView):
    """
    Autenticación mediante email y contraseña.
    Retorna un par de tokens JWT (access y refresh).
    """

    serializer_class = EmailTokenObtainPairSerializer


class PasswordResetViewSet(viewsets.ViewSet):
    """
    Recuperación de contraseña mediante email.
    Envia un correo con un código OTP y retorna un mensaje de seguridad.
    Valida el código y retorna un token de recuperación.
    Valida el token y permite cambiar la contraseña.
    """

    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "request":
            return PasswordResetRequestSerializer
        elif self.action == "verify":
            return PasswordResetVerifySerializer
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
                {"detail": "If the email address exists, you will receive a code."},
                status=status.HTTP_200_OK,
            )

        if user.role.name.lower() != "admin":
            return Response(
                {"detail": "Only administrators are allowed this action."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        PasswordResetOTP.objects.filter(email=email, is_used=False).update(is_used=True)

        otp = generate_otp()
        otp_hash = sha256(otp.encode()).hexdigest()
        expires_at = timezone.now() + timedelta(minutes=15)

        PasswordResetOTP.objects.create(
            user=user, email=email, otp_hash=otp_hash, expires_at=expires_at
        )

        send_reset_password_email(email, otp)

        return Response(
            {"detail": "If the email address exists, you will receive a code."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def verify(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        record = PasswordResetOTP.objects.filter(email=email, is_used=False).first()

        if not record:
            return Response(
                {"detail": "Invalid or expired code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if record.expires_at and timezone.now() > record.expires_at:
            return Response(
                {"detail": "Expired code."}, status=status.HTTP_400_BAD_REQUEST
            )

        if sha256(otp.encode()).hexdigest() != record.otp_hash:
            return Response(
                {"detail": "Invalid code."}, status=status.HTTP_400_BAD_REQUEST
            )

        record.reset_token = uuid.uuid4()
        record.save(update_fields=["reset_token"])

        return Response(
            {"reset_token": str(record.reset_token)}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"])
    def confirm(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_token = serializer.validated_data["reset_token"]
        new_password = serializer.validated_data["new_password"]

        record = PasswordResetOTP.objects.filter(
            reset_token=reset_token, is_used=False
        ).first()

        if not record:
            return Response(
                {"detail": "Invalid or expired reset token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=record.email).first()

        if not user:
            return Response(
                {"detail": "Invalid user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        record.is_used = True
        record.reset_token = None
        record.save(update_fields=["is_used", "reset_token"])

        return Response(
            {"detail": "Password updated successfully"},
            status=status.HTTP_200_OK,
        )
