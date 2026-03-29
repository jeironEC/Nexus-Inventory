# DRF
from rest_framework import serializers

# Python
from decimal import Decimal

# Django
from django.db import models

# Models
from nexus_inventory_backend.db.models import Product, SaleDetail


class SaleReturnDetailCreateSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
    )
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal("0.01")
    )

    def validate(self, attrs):
        sale_id = self.context.get("sale_id")
        product = attrs["product"]
        quantity = attrs["quantity"]

        sold_quantity = (
            SaleDetail.objects.filter(sale_id=sale_id, product=product).aggregate(
                total=models.Sum("quantity")
            )["total"]
            or 0
        )

        returned_quantity = self.context.get("returned_quantities", {}).get(
            product.id, 0
        )

        max_returnable = sold_quantity - returned_quantity

        if quantity > max_returnable:
            raise serializers.ValidationError(
                f"Cannot return more than {max_returnable} units for product '{product.name}'. "
                f"Sold: {sold_quantity}, Already returned: {returned_quantity}."
            )

        return attrs
