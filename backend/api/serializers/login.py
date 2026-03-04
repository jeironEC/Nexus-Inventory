# Django
from django.contrib.auth import authenticate

# Rest framework
from rest_framework import serializers


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

        if getattr(user, "is_active", False):
            raise serializers.ValidationError("Inactive user.")

        if getattr(user, "deleted", False):
            raise serializers.ValidationError("User account deleted.")

        data["user"] = user
        return data
