# Django
import django_filters

# Models
from nexus_inventory_backend.db.models import Category

# Filters
from .base import AuditFilter


class CategoryFilter(django_filters.FilterSet):
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
        model = Category
        fields = [
            "is_active",
            "name",
            "date_from",
            "date_to",
        ]


class CategoryAdminFilter(AuditFilter, CategoryFilter):
    class Meta(CategoryFilter.Meta):
        pass
