# DRF
from rest_framework import serializers

# Models
from nexus_inventory_backend.db.models import Customer

# Mixins
from api.mixins.audit_fields import AuditFieldsMixin


class CustomerSerializer(AuditFieldsMixin):
    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
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
        email = data.get("email")
        is_create = not self.instance

        if is_create and not email:
            raise serializers.ValidationError({"email": "Email is required."})

        if email:
            queryset = Customer.objects.filter(email__iexact=email)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError(
                    {"email": "A customer with this email already exists."}
                )

        return data
