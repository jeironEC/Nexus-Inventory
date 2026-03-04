# Rest framework
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import User


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
        ]

        def validate_email(self, value):
            user = (
                User.objects.filter(email=value).exclude(id=self.instance.id).exists()
            )

            if user:
                raise serializers.ValidationError("Email already in use.")
            return value
