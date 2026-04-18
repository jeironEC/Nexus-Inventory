# DRF
from rest_framework import serializers

# Python
import uuid

# Django
from django.db import transaction

# Models
from nexus_inventory_backend.db.models import (
    Company,
    Purchase,
    PurchaseDetail,
    InventoryMovement,
    Supplier,
    Invoice,
    Inventory,
)

# Enums
from nexus_inventory_backend.db.enums import MovementType, InvoiceType, InvoiceState

# Serializers
from api.serializers.purchase_detail_create import PurchaseDetailCreateSerializer


class PurchaseCreateSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        source="company",
        required=False,
        allow_null=True,
    )
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        source="supplier",
    )
    details = PurchaseDetailCreateSerializer(many=True)

    class Meta:
        model = Purchase
        fields = [
            "id",
            "company_id",
            "supplier_id",
            "details",
        ]
        read_only_fields = ["id"]

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

            inventory, created = Inventory.objects.get_or_create(
                product=product, defaults={"quantity": 0}
            )
            inventory.quantity += quantity
            inventory.save()

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
            company=purchase.company,
            invoice_type=InvoiceType.PURCHASE,
            number_invoice=f"PINV-{purchase.pk:08d}-{uuid.uuid4().hex[:6].upper()}",
            state=InvoiceState.ISSUED,
            created_by=user,
        )

        return purchase
