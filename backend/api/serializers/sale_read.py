# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Sale

# Serializers
from api.serializers.user_read import UserReadSerializer
from api.serializers.company import CompanySerializer
from api.serializers.customer import CustomerSerializer


class SaleReadSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    user = UserReadSerializer(read_only=True)
    updated_by = UserReadSerializer(read_only=True)
    deleted_by = UserReadSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = [
            "id",
            "company",
            "customer",
            "user",
            "discount_amount",
            "subtotal",
            "tax_percentage",
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
