# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Role

# Mixins
from api.mixins.audit_fields import AuditFieldsMixin


class RoleSerializer(AuditFieldsMixin):
    class Meta:
        model = Role
        fields = [
            "id",
            "name",
            "description",
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

    def validate_name(self, value):
        queryset = Role.objects.filter(name__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("A role with this name already exists.")

        return value
