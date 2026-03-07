# Rest framework
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
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate_name(self, value):
        queryset = Role.objects.filter(name__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("A role with this name already exists.")

        return value
