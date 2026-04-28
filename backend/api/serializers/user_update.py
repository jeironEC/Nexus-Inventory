# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import User


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "nif",
            "role",
        ]

    def validate_email(self, value):
        if not value:
            return value
        user = User.objects.filter(email=value).exclude(id=self.instance.id).exists()
        if user:
            raise serializers.ValidationError("Email already in use.")
        return value

    def validate_role(self, value):
        if value is None:
            return value
        request = self.context.get("request")
        if isinstance(value, int):
            from nexus_inventory_backend.db.models import Role

            try:
                role_obj = Role.objects.get(id=value)
                role_name = role_obj.name
            except Role.DoesNotExist:
                raise serializers.ValidationError("Role does not exist.")
        else:
            role_name = value.name if hasattr(value, "name") else None

        if role_name == "admin" and not request.user.role.name == "admin":
            raise serializers.ValidationError("You cannot assign admin role.")
        return value
