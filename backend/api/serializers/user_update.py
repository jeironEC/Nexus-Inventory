# DRF
from rest_framework import serializers

# Django
from django.contrib.auth.password_validation import validate_password

# Models
from nexus_inventory_backend.db.models import User, Role


class UserUpdateSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "nif",
            "role",
        ]

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_nif(self, value):
        queryset = User.objects.filter(nif__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("A User with this nif already exists.")
        return value

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

        if not request or not getattr(request, "user", None):
            return value

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
