# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Sale

# Serializers
from api.serializers.user_read import UserReadSerializer
from api.serializers.customer import CustomerSerializer


class SaleReadSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    user = UserReadSerializer(read_only=True)
    updated_by = UserReadSerializer(read_only=True)
    deleted_by = UserReadSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = [
            "id",
            "customer",
            "user",
            "subtotal",
            "tax_amount",
            "total_amount",
            "payment_method",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
            "updated_by",
            "deleted_by",
        ]
        read_only_fields = [
            "id",
            "subtotal",
            "tax_amount",
            "total_amount",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
