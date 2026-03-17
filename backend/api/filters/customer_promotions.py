# Django
import django_filters

# Models
from nexus_inventory_backend.db.models import CustomerPromotion

# Filters
from .base import AuditFilter


class CustomerPromotionFilter(django_filters.FilterSet):
    # Filters
    customer_id = django_filters.NumberFilter(field_name="customer_id")
    promotion_id = django_filters.NumberFilter(field_name="promotion_id")
    applied = django_filters.BooleanFilter(field_name="applied")

    # Searchs
    customer_email = django_filters.CharFilter(
        field_name="customer__email", lookup_expr="icontains"
    )
    promotion_name = django_filters.CharFilter(
        field_name="promotion__name", lookup_expr="icontains"
    )

    # Rangs
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )

    class Meta:
        model = CustomerPromotion
        fields = [
            "customer_id",
            "promotion_id",
            "applied",
            "customer_email",
            "promotion_name",
            "date_from",
            "date_to",
        ]


class CustomerPromotionAdminFilter(AuditFilter, CustomerPromotionFilter):
    class Meta(CustomerPromotionFilter.Meta):
        pass
