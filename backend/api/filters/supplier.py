# Django
import django_filters

# Models
from nexus_inventory_backend.db.models import Supplier

# Filters
from .base import AuditFilter


class SupplierFilter(django_filters.FilterSet):
    # Filters
    is_active = django_filters.BooleanFilter(field_name="is_active")

    # Searchs
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")

    # Rangs
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )

    class Meta:
        model = Supplier
        fields = [
            "is_active",
            "name",
            "email",
            "date_from",
            "date_to",
        ]


class SupplierAdminFilter(AuditFilter, SupplierFilter):
    class Meta(SupplierFilter.Meta):
        pass
