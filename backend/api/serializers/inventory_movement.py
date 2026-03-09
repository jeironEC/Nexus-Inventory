# DRF
from rest_framework import serializers

# Serializers
from .product import ProductSerializer
from .user_read import UserReadSerializer

# Models
from nexus_inventory_backend.db.models import InventoryMovement


class InventoryMovementSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserReadSerializer(read_only=True)

    class Meta:
        model = InventoryMovement
        fields = [
            "id",
            "product",
            "user",
            "quantity",
            "created_at",
        ]
        read_only_fields = fields
