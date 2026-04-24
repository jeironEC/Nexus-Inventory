# Django
import django_filters
from django.db.models import Q

# Models
from nexus_inventory_backend.db.models import Customer

# Filters
from .base import AuditFilter


class CustomerFilter(django_filters.FilterSet):
    # Filters
    is_active = django_filters.BooleanFilter(field_name="is_active")

    # Searchs
    full_name = django_filters.CharFilter(method="filter_full_name")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")

    # Rangs
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )

    def filter_full_name(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )

    class Meta:
        model = Customer
        fields = [
            "is_active",
            "full_name",
            "email",
            "date_from",
            "date_to",
        ]


class CustomerAdminFilter(AuditFilter, CustomerFilter):
    class Meta(CustomerFilter.Meta):
        pass
