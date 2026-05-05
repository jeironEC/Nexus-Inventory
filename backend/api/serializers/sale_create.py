from decimal import Decimal
from rest_framework import serializers

from nexus_inventory_backend.db.models import Company, Customer

from .sale_detail_create import SaleDetailCreateSerializer
from ..services.operation_service import create_sale


class SaleCreateSerializer(serializers.Serializer):
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
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        required=False,
        allow_null=True,
    )
    customer_id = serializers.PrimaryKeyRelatedField(
        source="customer",
        queryset=Customer.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    payment_method = serializers.ChoiceField(
        choices=["CASH", "CARD", "TRANSFER"],
        required=False,
        allow_null=True,
    )
    tax_percentage = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("21.00"),
    )
    details = SaleDetailCreateSerializer(many=True)

    def validate_details(self, value):
        if not value:
            raise serializers.ValidationError("At least one detail is required.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop("details")
        tax_percentage = validated_data.pop("tax_percentage", Decimal("21.00"))
        user = self.context["request"].user

        return create_sale(
            details_data=details_data,
            tax_percentage=tax_percentage,
            user=user,
            **validated_data,
        )

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
