# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Promotion


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = [
            "id",
            "name",
            "description",
            "discount_percentage",
            "start_date",
            "end_date",
            "state",
        ]
        read_only_fields = [
            "id",
            "state",
        ]
