# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import SaleReturnDetail

# Serializers
from .product import ProductSerializer
from .inventory_movement import InventoryMovementSerializer


class SaleReturnDetailReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    inventory_movement = InventoryMovementSerializer(read_only=True)

    class Meta:
        model = SaleReturnDetail
        fields = [
            "id",
            "product",
            "inventory_movement",
            "quantity",
            "unit_price",
            "subtotal",
            "created_at",
        ]
