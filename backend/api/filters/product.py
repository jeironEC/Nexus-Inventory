# Django
import django_filters

# Models
from nexus_inventory_backend.db.models import Product

# Filters
from .base import AuditFilter


class ProductFilter(django_filters.FilterSet):
    # Filters
    category_id = django_filters.NumberFilter(field_name="category_id")
    is_active = django_filters.BooleanFilter(field_name="is_active")

    # Searchs
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    unique_code = django_filters.CharFilter(
        field_name="unique_code", lookup_expr="icontains"
    )

    # Rangs
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )
    sale_price_min = django_filters.NumberFilter(
        field_name="sale_price", lookup_expr="gte"
    )
    sale_price_max = django_filters.NumberFilter(
        field_name="sale_price", lookup_expr="lte"
    )

    class Meta:
        model = Product
        fields = [
            "category_id",
            "is_active",
            "name",
            "unique_code",
            "date_from",
            "date_to",
            "sale_price_min",
            "sale_price_max",
        ]


class ProductAdminFilter(AuditFilter, ProductFilter):
    class Meta(ProductFilter.Meta):
        pass
