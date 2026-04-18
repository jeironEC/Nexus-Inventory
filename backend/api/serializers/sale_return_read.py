# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import SaleReturn

# Serializers
from api.serializers.user_read import UserReadSerializer
from api.serializers.sale_read import SaleReadSerializer


class SaleReturnReadSerializer(serializers.ModelSerializer):
    sale = SaleReadSerializer(read_only=True)
    user = UserReadSerializer(read_only=True)
    updated_by = UserReadSerializer(read_only=True)
    deleted_by = UserReadSerializer(read_only=True)

    class Meta:
        model = SaleReturn
        fields = [
            "id",
            "sale",
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
