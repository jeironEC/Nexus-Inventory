# Django
import django_filters
from django.db.models import Q

# Models
from nexus_inventory_backend.db.models import User

# Enums
from nexus_inventory_backend.db.enums import State

# Filters
from .base import AuditFilter


class UserFilter(django_filters.FilterSet):
    # Filters
    role_id = django_filters.NumberFilter(field_name="role__id")
    state = django_filters.ChoiceFilter(field_name="state", choices=State.choices)

    # Searchs
    full_name = django_filters.CharFilter(method="filter_full_name")

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
        model = User
        fields = [
            "role_id",
            "full_name",
            "state",
            "date_from",
            "date_to",
        ]


class UserAdminFilter(AuditFilter, UserFilter):
    class Meta(UserFilter.Meta):
        pass
