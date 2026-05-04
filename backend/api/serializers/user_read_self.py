# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import User


class UserReadSelf(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "nif",
            "first_name",
            "last_name",
            "email",
        ]
