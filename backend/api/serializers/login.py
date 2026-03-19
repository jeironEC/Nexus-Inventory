# DRF
from rest_framework import serializers

# Django
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError("Incorrect credentials.")

        if not user.is_active:
            raise serializers.ValidationError("Inactive user.")

        if getattr(user, "is_active", False):
            raise serializers.ValidationError("Inactive user.")

        if getattr(user, "deleted_at", None):
            raise serializers.ValidationError("User account deleted.")

        data["user"] = user
        return data
