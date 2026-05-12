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

    # Determina el origen del movimiento basado en las relaciones inversas
    source = serializers.SerializerMethodField()

    class Meta:
        model = InventoryMovement
        fields = [
            "id",
            "product",
            "product_id",
            "user",
            "user_id",
            "movement_type",
            "quantity",
            "created_at",
            "source",
        ]
        read_only_fields = [
            "id",
            "product",
            "product_id",
            "user",
            "user_id",
            "movement_type",
            "quantity",
            "created_at",
            "source",
        ]

    def get_source(self, obj):
        if hasattr(obj, "sale_detail"):
            return "VENTA"
        if hasattr(obj, "purchase_detail"):
            return "COMPRA"
        if hasattr(obj, "sale_return_detail"):
            return "DEVOLUCION_VENTA"
        if hasattr(obj, "purchase_return_detail"):
            return "DEVOLUCION_COMPRA"
        return "MANUAL"
