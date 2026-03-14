# DRF
from rest_framework import serializers

# Serializers
from .product import ProductSerializer

# Models
from nexus_inventory_backend.db.models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "product",
            "quantity",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "product",
            "quantity",
            "updated_at",
        ]
