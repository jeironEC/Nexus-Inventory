# Django
import django_filters

# Models
from nexus_inventory_backend.db.models import Customer

# Enums
from nexus_inventory_backend.db.enums import State


class CustomerFilter(django_filters.FilterSet):
    state = django_filters.ChoiceFilter(field_name="state", choices=State.choices)
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Customer
        fields = [
            "state",
            "date_from",
            "date_to",
        ]
