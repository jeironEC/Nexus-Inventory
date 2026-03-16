# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import User

# Serializers
from .user_role_read import UserRoleSerializer


class UserReadSerializer(serializers.ModelSerializer):
    role = UserRoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "role",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def get_fields(self):
        fields = super().get_fields()

        for field in fields.values():
            field.read_only = True
        return fields
