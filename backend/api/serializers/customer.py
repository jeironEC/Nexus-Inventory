# DRF

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
