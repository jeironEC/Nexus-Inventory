# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Promotion

# Serializers
from .user_read import UserReadSerializer


class PromotionSerializer(serializers.ModelSerializer):
    created_by = UserReadSerializer(read_only=True)
    updated_by = UserReadSerializer(read_only=True)
    deleted_by = UserReadSerializer(read_only=True)

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
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
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
