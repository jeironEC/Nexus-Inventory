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
            "tax_id",
            "name",
            "address",
            "number_phone",
            "email",
            "website",
            "logo",
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

    def validate_tax_id(self, value):
        queryset = Company.objects.filter(tax_id__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "A Company with this tax id already exists."
            )
        return value
