# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import PurchaseDetail

# Serializers
from .product import ProductSerializer
from .inventory_movement import InventoryMovementSerializer


class PurchaseDetailReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    inventory_movement = InventoryMovementSerializer(read_only=True)

    class Meta:
        model = PurchaseDetail
        fields = [
            "id",
            "product",
            "inventory_movement",
            "quantity",
            "unit_cost",
            "subtotal",
            "created_at",
        ]
