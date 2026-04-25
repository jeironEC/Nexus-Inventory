# Django
import django_filters

# Models
from nexus_inventory_backend.db.models import Company

# Filters
from .base import AuditFilter


class CompanyFilter(django_filters.FilterSet):
    # Filters
    is_active = django_filters.BooleanFilter(field_name="is_active")

    # Searchs
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    # Rangs
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )

    class Meta:
        model = Company
        fields = [
            "is_active",
            "name",
            "date_from",
            "date_to",
        ]


class CompanyAdminFilter(AuditFilter, CompanyFilter):
    class Meta(CompanyFilter.Meta):
        pass
