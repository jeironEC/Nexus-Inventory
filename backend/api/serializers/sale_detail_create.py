# DRF
from rest_framework import serializers

# Python
from decimal import Decimal

# Models
from nexus_inventory_backend.db.models import Product


class SaleDetailCreateSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
    )
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal("0.01")
    )
