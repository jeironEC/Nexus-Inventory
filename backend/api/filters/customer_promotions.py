# Django
import django_filters

# Models
from nexus_inventory_backend.db.models import CustomerPromotion


class CustomerPromotionFilter(django_filters.FilterSet):
    applied = django_filters.BooleanFilter(field_name="applied")
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = CustomerPromotion
        fields = [
            "applied",
            "date_from",
            "date_to",
        ]
