from rest_framework import serializers

from nexus_inventory_backend.db.models import Sale
from nexus_inventory_backend.db.enums import OperationState

from .sale_return_detail_create import SaleReturnDetailCreateSerializer
from ..services.operation_service import create_sale_return


class SaleReturnCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    sale = serializers.PrimaryKeyRelatedField(
        queryset=Sale.objects.all(),
        required=False,
    )
    sale_id = serializers.PrimaryKeyRelatedField(
        source="sale",
        queryset=Sale.objects.all(),
        required=False,
        write_only=True,
    )
    sale_id = serializers.PrimaryKeyRelatedField(
        source="sale",
        queryset=Sale.objects.all(),
        required=False,
        write_only=True,
    )
    reason = serializers.CharField(max_length=255)
    details = SaleReturnDetailCreateSerializer(many=True)

    def validate(self, data):
        action = self.context.get("view").action if self.context.get("view") else None
        if action == "create" and not data.get("sale") and not data.get("sale_id"):
            raise serializers.ValidationError({"sale": "This field is required."})
        return data

    def validate_details(self, value):
        if not value:
            raise serializers.ValidationError("At least one detail is required.")
        return value

    def validate_sale(self, value):
        if value and value.state == OperationState.CANCELED:
            raise serializers.ValidationError(
                "Cannot return items from a canceled sale."
            )
        return value

    def create(self, validated_data):
        details_data = validated_data.pop("details")
        if "sale_id" in validated_data:
            validated_data.pop("sale_id")
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
