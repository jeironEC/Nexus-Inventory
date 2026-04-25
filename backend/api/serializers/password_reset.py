# DRF
from rest_framework import serializers


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=6, max_length=6)


class PasswordResetConfirmSerializer(serializers.Serializer):
    reset_token = serializers.UUIDField()
    new_password = serializers.CharField(min_length=8, write_only=True)
