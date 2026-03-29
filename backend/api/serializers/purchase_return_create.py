# DRF
from rest_framework import serializers

# Django
from django.db import transaction

# Models
from nexus_inventory_backend.db.models import (
    PurchaseReturn,
    PurchaseReturnDetail,
    InventoryMovement,
    Purchase,
)

# Enums
from nexus_inventory_backend.db.enums import MovementType

# Serializers
from .purchase_return_detail_create import PurchaseReturnDetailCreateSerializer


class PurchaseReturnCreateSerializer(serializers.ModelSerializer):
    purchase_id = serializers.PrimaryKeyRelatedField(
        queryset=Purchase.objects.all(),
        source="purchase",
    )
    details = PurchaseReturnDetailCreateSerializer(many=True)

    class Meta:
        model = PurchaseReturn
        fields = [
            "purchase_id",
            "reason",
            "details",
        ]

    def validate_details(self, value):
        if not value:
            raise serializers.ValidationError("At least one detail is required.")
        return value

    def validate_purchase_id(self, value):
        if value.state == "CANCELED":
            raise serializers.ValidationError(
                "Cannot return items from a canceled purchase."
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        details_data = validated_data.pop("details")
        user = self.context["request"].user

        total_amount = sum(
            detail["quantity"] * detail["unit_cost"] for detail in details_data
        )

        purchase_return = PurchaseReturn.objects.create(
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
                movement_type=MovementType.OUT,
                quantity=quantity,
            )

            PurchaseReturnDetail.objects.create(
                purchase_return=purchase_return,
                product=product,
                inventory_movement=inventory_movement,
                quantity=quantity,
                unit_cost=unit_cost,
                subtotal=quantity * unit_cost,
            )

        return purchase_return
