# DRF

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
