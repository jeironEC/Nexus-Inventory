# DRF
from rest_framework import serializers

# Serializers
from .product import ProductSerializer
from .user_read import UserReadSerializer

# Models
from nexus_inventory_backend.db.models import InventoryMovement


class InventoryMovementSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=InventoryMovement._meta.get_field(
            "product"
        ).remote_field.model.objects.all(),
        source="product",
        write_only=True,
    )
    user = UserReadSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=InventoryMovement._meta.get_field(
            "user"
        ).remote_field.model.objects.all(),
        source="user",
        write_only=True,
    )

    source = serializers.CharField(read_only=True)

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
        read_only_fields = fields
