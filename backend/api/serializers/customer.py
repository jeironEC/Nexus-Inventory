# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "number_phone",
            "address",
            "state",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "state",
            "created_at",
            "updated_at",
        ]
