# DRF
from rest_framework import serializers

# Django
from django.db import transaction

# Models
from nexus_inventory_backend.db.models import (
    SaleReturn,
    SaleReturnDetail,
    InventoryMovement,
    Sale,
)

# Enums
from nexus_inventory_backend.db.enums import MovementType

# Serializers
from .sale_return_detail_create import SaleReturnDetailCreateSerializer


class SaleReturnCreateSerializer(serializers.ModelSerializer):
    sale_id = serializers.PrimaryKeyRelatedField(
        queryset=Sale.objects.all(),
        source="sale",
    )
    details = SaleReturnDetailCreateSerializer(many=True)

    class Meta:
        model = SaleReturn
        fields = [
            "sale_id",
            "reason",
            "details",
        ]

    def validate_details(self, value):
        if not value:
            raise serializers.ValidationError("At least one detail is required.")
        return value

    def validate_sale_id(self, value):
        if value.state == "CANCELED":
            raise serializers.ValidationError(
                "Cannot return items from a canceled sale."
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        details_data = validated_data.pop("details")
        user = self.context["request"].user

        total_amount = sum(
            detail["quantity"] * detail["unit_price"] for detail in details_data
        )

        sale_return = SaleReturn.objects.create(
            **validated_data,
            user=user,
            total_amount=total_amount,
        )

        for detail in details_data:
            product = detail["product"]
            quantity = detail["quantity"]
            unit_price = detail["unit_price"]

            inventory_movement = InventoryMovement.objects.create(
                product=product,
                user=user,
                movement_type=MovementType.IN,
                quantity=quantity,
            )

            SaleReturnDetail.objects.create(
                sale_return=sale_return,
                product=product,
                inventory_movement=inventory_movement,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=quantity * unit_price,
            )

        return sale_return
