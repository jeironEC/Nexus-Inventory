from rest_framework import serializers

from nexus_inventory_backend.db.models import Purchase
from nexus_inventory_backend.db.enums import OperationState

from .purchase_return_detail_create import PurchaseReturnDetailCreateSerializer
from ..services.operation_service import create_purchase_return


class PurchaseReturnCreateSerializer(serializers.Serializer):
    purchase = serializers.PrimaryKeyRelatedField(
        queryset=Purchase.objects.all(),
    )
    reason = serializers.CharField(max_length=255)
    details = PurchaseReturnDetailCreateSerializer(many=True)

    def validate_details(self, value):
        if not value:
            raise serializers.ValidationError("At least one detail is required.")
        return value

    def validate_purchase(self, value):
        if value.state == OperationState.CANCELED:
            raise serializers.ValidationError(
                "Cannot return items from a canceled purchase."
            )
        return value

    def create(self, validated_data):
        details_data = validated_data.pop("details")
        user = self.context["request"].user

        return create_purchase_return(
            details_data=details_data,
            user=user,
            **validated_data,
        )

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
