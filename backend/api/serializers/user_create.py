# Django
from django.db import transaction
from django.contrib.auth.password_validation import validate_password

# Rest framework
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "role",
        ]

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_role(self, value):
        request = self.context.get("request")

        if value.name == "admin" and not request.user.role.name == "admin":
            raise serializers.ValidationError("You cannot assign admin role.")
        return value

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create_user(**validated_data)
            return user
        except Exception as error:
            raise serializers.ValidationError({"detail": str(error)})
