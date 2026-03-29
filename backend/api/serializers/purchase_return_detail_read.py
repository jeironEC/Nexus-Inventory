# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import PurchaseReturnDetail

# Serializers
from .product import ProductSerializer
from .inventory_movement import InventoryMovementSerializer


class PurchaseReturnDetailReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    inventory_movement = InventoryMovementSerializer(read_only=True)

    class Meta:
        model = PurchaseReturnDetail
        fields = [
            "id",
            "product",
            "inventory_movement",
            "quantity",
            "unit_cost",
            "subtotal",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "inventory_movement",
            "subtotal",
            "created_at",
        ]
