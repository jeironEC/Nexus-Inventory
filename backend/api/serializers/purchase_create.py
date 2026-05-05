from rest_framework import serializers

from nexus_inventory_backend.db.models import Company, Supplier

from .purchase_detail_create import PurchaseDetailCreateSerializer
from ..services.operation_service import create_purchase


class PurchaseCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        required=False,
        allow_null=True,
    )
    company_id = serializers.PrimaryKeyRelatedField(
        source="company",
        queryset=Company.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
    )
    supplier_id = serializers.PrimaryKeyRelatedField(
        source="supplier",
        queryset=Supplier.objects.all(),
        required=False,
        write_only=True,
    )
    details = PurchaseDetailCreateSerializer(many=True)

    def validate(self, data):
        if not data.get("supplier") and not data.get("supplier_id"):
            raise serializers.ValidationError({"supplier": "This field is required."})
        return data

    def validate_details(self, value):
        if not value:
            raise serializers.ValidationError("At least one detail is required.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop("details")
        if "supplier_id" in validated_data:
            validated_data.pop("supplier_id")
        if "company_id" in validated_data:
            validated_data.pop("company_id")
        user = self.context["request"].user

        return create_purchase(
            details_data=details_data,
            user=user,
            **validated_data,
        )

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
