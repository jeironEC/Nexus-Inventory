# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Promotion, CustomerPromotion


class CustomerPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPromotion
        fields = [
            "id",
            "customer",
            "promotion",
            "applied",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

        def validate(self, data):
            customer = data.get("customer")
            promotion = data.get("promotion")

            if CustomerPromotion.objects.filter(
                customer=customer, promotion=promotion
            ).exists():
                raise serializers.ValidationError(
                    "This promotion is already assigned to the customer."
                )

            return data


class CustomerPromotionCreateSerializer(serializers.Serializer):
    promotion = serializers.IntegerField()

    def validate_promotion(self, value):
        if not Promotion.objects.filter(id=value).exists():
            raise serializers.ValidationError("Promotion not found")
        return value

    def validate(self, data):
        customer = self.context.get("customer")
        promotion_id = data.get("promotion")

        if (
            customer
            and CustomerPromotion.objects.filter(
                customer=customer, promotion_id=promotion_id
            ).exists()
        ):
            raise serializers.ValidationError(
                "This promotion is already assigned to the customer."
            )

        return data
