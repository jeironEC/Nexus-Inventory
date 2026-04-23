# DRF
from rest_framework import serializers

# Python
import uuid
from decimal import Decimal

# Django
from django.db import transaction

# Models
from nexus_inventory_backend.db.models import (
    Company,
    Sale,
    SaleDetail,
    InventoryMovement,
    Customer,
    Invoice,
    Inventory,
)

# Enums
from nexus_inventory_backend.db.enums import (
    MovementType,
    InvoiceState,
    InvoiceType,
)

# Serializers
from .sale_detail_create import SaleDetailCreateSerializer


class SaleCreateSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        source="company",
        required=False,
        allow_null=True,
    )
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
            "id",
            "company_id",
            "customer_id",
            "payment_method",
            "tax_percentage",
            "tax_percentage",
            "details",
        ]
        read_only_fields = ["id", "tax_percentage"]

    def validate_details(self, value):
        if not value:
            raise serializers.ValidationError("At least one detail is required.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        details_data = validated_data.pop("details")
        user = self.context["request"].user

        # Calcular totales
        subtotal = Decimal("0.00")
        discount_amount = Decimal("0.00")

        # Pre-validar stock de productos
        stock_errors = []

        for detail in details_data:
            product = detail["product"]
            quantity = detail["quantity"]
            unit_price = detail["unit_price"]

            # Verificar stock disponible
            try:
                inventory = Inventory.objects.get(product=product)

                if inventory.quantity < quantity:
                    stock_errors.append(
                        {
                            "product_id": product.id,
                            "product_name": product.name,
                            "requested": quantity,
                            "available": inventory.quantity,
                        }
                    )
            except Inventory.DoesNotExist:
                stock_errors.append(
                    {
                        "product_id": product.id,
                        "product_name": product.name,
                        "error": "Product without inventory",
                    }
                )

        if stock_errors:
            raise serializers.ValidationError(
                {"details": "Stock insufficient", "errors": stock_errors}
            )

        # Calcular descuentos y totales
        for detail in details_data:
            product = detail["product"]
            quantity = detail["quantity"]
            unit_price = detail["unit_price"]

            # Descuento de producto
            product_discount = Decimal("0.00")

            if product.discount_percentage and product.discount_percentage > 0:
                product_discount = (
                    unit_price * product.discount_percentage / 100
                ) * quantity

            # Precio con descuento
            unit_price_final = unit_price - (
                unit_price * (product.discount_percentage or 0) / 100
            )

            subtotal += quantity * unit_price_final
            discount_amount += product_discount

        total_discount = discount_amount
        tax_base = subtotal - total_discount

        tax_percentage = validated_data.get("tax_percentage", Decimal("21.00"))
        tax_amount = (tax_base * tax_percentage / 100).quantize(Decimal("0.01"))
        total_amount = tax_base + tax_amount

        # Crear venta
        sale = Sale.objects.create(
            **validated_data,
            user=user,
            discount_amount=total_discount,
            subtotal=subtotal,
            tax_percentage=tax_percentage,
            tax_amount=tax_amount,
            total_amount=total_amount,
        )

        # Crear detalles y movimientos de inventario
        for detail in details_data:
            product = detail["product"]
            quantity = detail["quantity"]
            unit_price = detail["unit_price"]

            # Precio con descuento aplicado
            unit_price_final = unit_price

            if product.discount_percentage and product.discount_percentage > 0:
                unit_price_final = unit_price - (
                    unit_price * product.discount_percentage / 100
                )

            inventory_movement = InventoryMovement.objects.create(
                product=product,
                user=user,
                movement_type=MovementType.OUT,
                quantity=quantity,
            )

            inventory = Inventory.objects.get(product=product)
            inventory.quantity -= quantity
            inventory.save()

            SaleDetail.objects.create(
                sale=sale,
                product=product,
                inventory_movement=inventory_movement,
                quantity=quantity,
                unit_price=unit_price_final,
                subtotal=quantity * unit_price_final,
            )

        # Crear factura automáticamente
        Invoice.objects.create(
            sale=sale,
            company=sale.company,
            invoice_type=InvoiceType.SALE,
            number_invoice=f"SINV-{sale.pk:08d}-{uuid.uuid4().hex[:6].upper()}",
            state=InvoiceState.ISSUED,
            created_by=user,
        )

        return sale
