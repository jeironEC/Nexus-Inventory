# DRF
from rest_framework import serializers

# Django
from django.db import transaction
from django.contrib.auth.password_validation import validate_password

# Models
from nexus_inventory_backend.db.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "nif",
            "role",
        ]

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_nif(self, value):
        queryset = User.objects.filter(nif__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("A User with this nif already exists.")
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
