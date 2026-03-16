# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Customer

# Serializers
from .user_read import UserReadSerializer


class CustomerSerializer(serializers.ModelSerializer):
    created_by = UserReadSerializer(read_only=True)
    updated_by = UserReadSerializer(read_only=True)
    deleted_by = UserReadSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "number_phone",
            "address",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        ]
        read_only_fields = [
            "id",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
