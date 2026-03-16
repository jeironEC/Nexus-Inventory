# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Role


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            "id",
            "name",
            "description",
            "state",
        ]
