# DRF
from rest_framework import serializers

# Python
from decimal import Decimal

# Django
from django.db import transaction

# Models
from nexus_inventory_backend.db.models import (
    Sale,
    SaleDetail,
    InventoryMovement,
    Customer,
    Invoice,
)

# Enums
from nexus_inventory_backend.db.enums import MovementType, TaxRate, InvoiceState

# Serializers
from .sale_detail_create import SaleDetailCreateSerializer


class SaleCreateSerializer(serializers.ModelSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source="customer",
        required=False,
        allow_null=True,
    )
    details = SaleDetailCreateSerializer(many=True)

    class Meta:
        model = Sale
        fields = [
            "customer_id",
            "payment_method",
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

        # Calcular totales
        subtotal = sum(
            detail["quantity"] * detail["unit_price"] for detail in details_data
        )
        tax_amount = (subtotal * TaxRate.ESP).quantize(Decimal("0.01"))
        total_amount = subtotal + tax_amount

        # Crear venta
        sale = Sale.objects.create(
            **validated_data,
            user=user,
            subtotal=subtotal,
            tax_amount=tax_amount,
            total_amount=total_amount,
        )

        # Crear detalles y movimientos de inventario
        for detail in details_data:
            product = detail["product"]
            quantity = detail["quantity"]
            unit_price = detail["unit_price"]

            inventory_movement = InventoryMovement.objects.create(
                product=product,
                user=user,
                movement_type=MovementType.OUT,
                quantity=quantity,
            )

            SaleDetail.objects.create(
                sale=sale,
                product=product,
                inventory_movement=inventory_movement,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=quantity * unit_price,
            )

        # Crear factura automáticamente
        Invoice.objects.create(
            sale=sale,
            number_invoice=f"INV-{sale.pk:08d}",
            state=InvoiceState.ISSUED,
            created_by=user,
        )

        return sale
