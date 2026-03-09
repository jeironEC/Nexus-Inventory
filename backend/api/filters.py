# Django
import django_filters

# Models
from nexus_inventory_backend.db.models import InventoryMovement


class InventoryMovementFilter(django_filters.FilterSet):
    product_id = django_filters.NumberFilter(field_name="product_id")
    user_id = django_filters.NumberFilter(field_name="user_id")
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = InventoryMovement
        fields = [
            "product_id",
            "user_id",
            "date_from",
            "date_to",
        ]
