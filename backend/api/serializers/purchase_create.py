# DRF
from rest_framework import serializers

# Python
from decimal import Decimal

# Django
from django.db import transaction

# Models
from nexus_inventory_backend.db.models import (
    Purchase,
    PurchaseDetail,
    InventoryMovement,
    Supplier,
    Invoice,
)

# Enums
from nexus_inventory_backend.db.enums import MovementType, InvoiceType, InvoiceState

# Serializers
# DRF

# Models
from nexus_inventory_backend.db.models import Product


# Provisional
class PurchaseDetailCreateSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
    )
    quantity = serializers.IntegerField(min_value=1)
    unit_cost = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal("0.01")
    )


class PurchaseCreateSerializer(serializers.ModelSerializer):
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        source="supplier",
    )
    details = PurchaseDetailCreateSerializer(many=True)

    class Meta:
        model = Purchase
        fields = [
            "supplier_id",
            "details",
        ]

    def validate_details(self, value):
        if not value:
            raise serializers.ValidationError("At least one detail is required.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        details_data = validated_data.pop("details")
        user = self.context["request"].user

        total_amount = sum(
            detail["quantity"] * detail["unit_cost"] for detail in details_data
        )

        purchase = Purchase.objects.create(
            **validated_data,
            user=user,
            total_amount=total_amount,
        )

        for detail in details_data:
            product = detail["product"]
            quantity = detail["quantity"]
            unit_cost = detail["unit_cost"]

            inventory_movement = InventoryMovement.objects.create(
                product=product,
                user=user,
                movement_type=MovementType.IN,
                quantity=quantity,
            )

            PurchaseDetail.objects.create(
                purchase=purchase,
                product=product,
                inventory_movement=inventory_movement,
                quantity=quantity,
                unit_cost=unit_cost,
                subtotal=quantity * unit_cost,
            )

            Invoice.objects.create(
                purchase=purchase,
                invoice_type=InvoiceType.PURCHASE,
                number_invoice=f"PINV-{purchase.pk:08d}",
                state=InvoiceState.ISSUED,
                created_by=user,
            )

        return purchase
