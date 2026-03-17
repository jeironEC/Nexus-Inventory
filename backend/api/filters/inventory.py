# Django
import django_filters

# Models
from nexus_inventory_backend.db.models import Inventory

# Filters
from .base import AuditFilter


class InventoryFilter(django_filters.FilterSet):
    # Filters
    product_id = django_filters.NumberFilter(field_name="product_id")

    # Searchs
    product_name = django_filters.CharFilter(
        field_name="product__name", lookup_expr="icontains"
    )

    # Rangs
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )
    quantity_min = django_filters.NumberFilter(field_name="quantity", lookup_expr="gte")
    quantity_max = django_filters.NumberFilter(field_name="quantity", lookup_expr="lte")

    class Meta:
        model: Inventory
        fields = [
            "product_id",
            "product_name",
            "date_from",
            "date_to",
            "quantity_min",
            "quantity_max",
        ]


class InventoryAdminFilter(AuditFilter, InventoryFilter):
    class Meta(InventoryFilter.Meta):
        pass
