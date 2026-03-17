# Django
import django_filters

# Models
from nexus_inventory_backend.db.models import Role

# Enums
from nexus_inventory_backend.db.enums import State

# Filters
from .base import AuditFilter


class RoleFilter(django_filters.FilterSet):
    # Filters
    state = django_filters.ChoiceFilter(field_name="state", choices=State.choices)

    # Searchs
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    # Rangs
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Role
        fields = [
            "name",
            "state",
            "date_from",
            "date_to",
        ]


class RoleAdminFilter(AuditFilter, RoleFilter):
    class Meta(RoleFilter.Meta):
        pass
