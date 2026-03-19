# DRF

# Models
from nexus_inventory_backend.db.models import Promotion

# Mixins
from api.mixins.audit_fields import AuditFieldsMixin


class PromotionSerializer(AuditFieldsMixin):
    class Meta:
        model = Promotion
        fields = [
            "id",
            "name",
            "description",
            "discount_percentage",
            "start_date",
            "end_date",
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
