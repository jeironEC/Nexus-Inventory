# Django
import django_filters

# Models
from nexus_inventory_backend.db.models import Promotion

# Enums
from nexus_inventory_backend.db.enums import State


class PromotionFilter(django_filters.FilterSet):
    state = django_filters.ChoiceFilter(field_name="state", choices=State.choices)
    start_date = django_filters.DateFilter(field_name="start_date")
    end_date = django_filters.DateFilter(field_name="end_date")
    discount_percentage = django_filters.NumberFilter(field_name="discount_percentage")

    class Meta:
        model = Promotion
        fields = [
            "state",
            "discount_percentage",
            "start_date",
            "end_date",
        ]
