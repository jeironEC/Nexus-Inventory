# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Supplier

# Mixins
from api.mixins.audit_fields import AuditFieldsMixin


class SupplierSerializer(AuditFieldsMixin):
    class Meta:
        model = Supplier
        fields = [
            "id",
            "name",
            "email",
            "nif",
            "number_phone",
            "address",
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

    def validate(self, data):
        name = data.get("name")
        nif = data.get("nif")
        is_create = not self.instance

        if is_create and not name:
            raise serializers.ValidationError({"name": "Name is required."})

        if name:
            queryset = Supplier.objects.filter(name__iexact=name)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError(
                    {"name": "A supplier with this name already exists."}
                )

        if nif:
            queryset = Supplier.objects.filter(nif__iexact=nif)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError(
                    {"nif": "A supplier with this nif already exists."}
                )

        return data
