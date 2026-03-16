# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Promotion, Customer, CustomerPromotion

# Serializers
from .user_read import UserReadSerializer
from .customer import CustomerSerializer
from .promotion import PromotionSerializer


class CustomerPromotionSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source="customer", write_only=True
    )
    promotion = PromotionSerializer(read_only=True)
    promotion_id = serializers.PrimaryKeyRelatedField(
        queryset=Promotion.objects.all(), source="promotion", write_only=True
    )
    created_by = UserReadSerializer(read_only=True)
    updated_by = UserReadSerializer(read_only=True)
    deleted_by = UserReadSerializer(read_only=True)

    class Meta:
        model = CustomerPromotion
        fields = [
            "id",
            "customer",
            "customer_id",
            "promotion",
            "promotion_id",
            "applied",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def validate(self, data):
        customer = data.get("customer")
        promotion = data.get("promotion")

        if customer and promotion:
            queryset = CustomerPromotion.objects.filter(
                customer=customer, promotion=promotion
            )

            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise serializers.ValidationError(
                    "This promotion is already assigned to the customer."
                )

        return data


class CustomerPromotionCreateSerializer(serializers.ModelSerializer):
    promotion = serializers.PrimaryKeyRelatedField(queryset=Promotion.objects.all())

    class Meta:
        model = CustomerPromotion
        fields = ["promotion"]

    def validate(self, data):
        customer = self.context.get("customer")
        promotion = data["promotion"]

        if CustomerPromotion.objects.filter(
            customer=customer, promotion=promotion
        ).exists():
            raise serializers.ValidationError(
                {"promotion": "This promotion is already assigned to the customer."}
            )

        return data
