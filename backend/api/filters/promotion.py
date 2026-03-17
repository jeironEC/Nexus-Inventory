# Django
import django_filters

# Models
from nexus_inventory_backend.db.models import Promotion

# Enums
from nexus_inventory_backend.db.enums import State

# Filters
from .base import AuditFilter


class PromotionFilter(django_filters.FilterSet):
    # Filters
    state = django_filters.ChoiceFilter(field_name="state", choices=State.choices)

    # Searchs
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    # Rangs
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )
    active_on = django_filters.DateFilter(method="filter_active_on")
    discount_min = django_filters.NumberFilter(
        field_name="discount_percentage", lookup_expr="gte"
    )
    discount_max = django_filters.NumberFilter(
        field_name="discount_percentage", lookup_expr="lte"
    )

    def filter_active_on(self, queryset, name, value):
        return queryset.filter(start_date__lte=value, end_date__gte=value)

    class Meta:
        model = Promotion
        fields = [
            "state",
            "name",
            "date_from",
            "date_to",
            "active_on",
            "discount_min",
            "discount_max",
        ]


class PromotionAdminFilter(AuditFilter, PromotionFilter):
    class Meta(PromotionFilter.Meta):
        pass
