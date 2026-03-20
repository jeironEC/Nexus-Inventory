# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import User, Customer, Sale

# Serializers
from api.serializers.user_read import UserReadSerializer
from api.serializers.customer import CustomerSerializer


class SaleSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source="customer",
        write_only=True,
        required=False,
        allow_null=True,
    )
    user = UserReadSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )
    updated_by = UserReadSerializer(read_only=True)
    deleted_by = UserReadSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = [
            "id",
            "customer",
            "customer_id",
            "user",
            "user_id",
            "subtotal",
            "tax_amount",
            "total_amount",
            "payment_method",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
            "updated_by",
            "deleted_by",
        ]
        read_only_fields = [
            "id",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def validate(self, data):
        subtotal = data.get("subtotal")
        tax_amount = data.get("tax_amount", 0)
        total_amount = data.get("total_amount")

        if subtotal is not None and subtotal < 0:
            raise serializers.ValidationError({"subtotal": "Subtotal must be >= 0."})

        if tax_amount is not None and tax_amount < 0:
            raise serializers.ValidationError(
                {"tax_amount": "Tax amount must be >= 0."}
            )

        if total_amount is not None and total_amount < 0:
            raise serializers.ValidationError(
                {"total_amount": "Total amount must be >= 0."}
            )

        if subtotal is not None and tax_amount is not None and total_amount is not None:
            expected_total = subtotal + tax_amount
            if total_amount != expected_total:
                raise serializers.ValidationError(
                    {
                        "total_amount": f"Total amount must equal subtotal + tax_amount ({expected_total})."
                    }
                )

        return data
