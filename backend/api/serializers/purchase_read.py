# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Purchase

# Serializers
from api.serializers.user_read import UserReadSerializer
from api.serializers.supplier import SupplierSerializer


class PurchaseReadSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)
    user = UserReadSerializer(read_only=True)
    updated_by = UserReadSerializer(read_only=True)
    deleted_by = UserReadSerializer(read_only=True)

    class Meta:
        model = Purchase
        fields = [
            "id",
            "supplier",
            "user",
            "total_amount",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
            "updated_by",
            "deleted_by",
        ]
