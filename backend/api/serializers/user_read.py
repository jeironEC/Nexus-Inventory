# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import User

# Serializers
from .user_role import RoleSerializer
from .user_read_self import UserReadSelf


class UserReadSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    created_by = UserReadSelf(read_only=True)
    updated_by = UserReadSelf(read_only=True)
    deleted_by = UserReadSelf(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "nif",
            "role",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        ]
