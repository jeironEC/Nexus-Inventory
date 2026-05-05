from rest_framework import serializers

from nexus_inventory_backend.db.models import Sale
from nexus_inventory_backend.db.enums import OperationState

from .sale_return_detail_create import SaleReturnDetailCreateSerializer
from ..services.operation_service import create_sale_return


class SaleReturnCreateSerializer(serializers.Serializer):
    sale = serializers.PrimaryKeyRelatedField(
        queryset=Sale.objects.all(),
    )
    reason = serializers.CharField(max_length=255)
    details = SaleReturnDetailCreateSerializer(many=True)

    def validate_details(self, value):
        if not value:
            raise serializers.ValidationError("At least one detail is required.")
        return value

    def validate_sale(self, value):
        if value.state == OperationState.CANCELED:
            raise serializers.ValidationError(
                "Cannot return items from a canceled sale."
            )
        return value

    def create(self, validated_data):
        details_data = validated_data.pop("details")
        user = self.context["request"].user

        return create_sale_return(
            details_data=details_data,
            user=user,
            **validated_data,
        )

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
