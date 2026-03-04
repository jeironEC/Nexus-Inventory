# Rest framework
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import User


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "updated_at"]
