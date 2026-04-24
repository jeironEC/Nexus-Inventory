# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Company

# Mixins
from api.mixins.audit_fields import AuditFieldsMixin


class CompanySerializer(AuditFieldsMixin):
    class Meta:
        model = Company
        fields = [
            "id",
            "nif",
            "name",
            "address",
            "number_phone",
            "email",
            "website",
            "logo",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
        ]
        read_only_fields = [
            "id",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def validate_nif(self, value):
        queryset = Company.objects.filter(nif__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("A Company with this nif already exists.")
        return value
