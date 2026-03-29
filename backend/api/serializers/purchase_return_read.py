# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import PurchaseReturn

# Serializers
from api.serializers.user_read import UserReadSerializer
from api.serializers.purchase_read import PurchaseReadSerializer


class PurchaseReturnReadSerializer(serializers.ModelSerializer):
    purchase = PurchaseReadSerializer(read_only=True)
    user = UserReadSerializer(read_only=True)
    updated_by = UserReadSerializer(read_only=True)
    deleted_by = UserReadSerializer(read_only=True)

    class Meta:
        model = PurchaseReturn
        fields = [
            "id",
            "purchase",
            "user",
            "reason",
            "total_amount",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
            "updated_by",
            "deleted_by",
        ]
        read_only_fields = [
            "id",
            "total_amount",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
