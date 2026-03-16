# DRF
from rest_framework import serializers

# Serializers
from .product import ProductSerializer
from .user_read import UserReadSerializer

# Models
from nexus_inventory_backend.db.models import User, Product, InventoryMovement


class InventoryMovementSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )
    user = UserReadSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )

    class Meta:
        model = InventoryMovement
        fields = [
            "id",
            "product",
            "product_id",
            "user",
            "user_id",
            "quantity",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "product",
            "product_id",
            "user",
            "user_id",
            "quantity",
            "created_at",
        ]
