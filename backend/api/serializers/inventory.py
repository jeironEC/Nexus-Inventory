# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Product, Inventory

# Serializers
from .user_read import UserReadSerializer
from .product import ProductSerializer


class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )
    created_by = UserReadSerializer(read_only=True)
    updated_by = UserReadSerializer(read_only=True)
    deleted_by = UserReadSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "product",
            "product_id",
            "quantity",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        ]
        read_only_fields = [
            "id",
            "quantity",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
