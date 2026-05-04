# Django
import django_filters

# Models
from nexus_inventory_backend.db.models import Sale

# Enums
from nexus_inventory_backend.db.enums import OperationState, PaymentMethod

# Filters


class SaleFilter(django_filters.FilterSet):
    # Filters
    state = django_filters.ChoiceFilter(
        field_name="state", choices=OperationState.choices
    )
    payment_method = django_filters.ChoiceFilter(
        field_name="payment_method", choices=PaymentMethod.choices
    )
    customer_id = django_filters.NumberFilter(field_name="customer__id")

    # Rangs
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )

    def filter_customer(self, queryset, name, value):
        if value.lower() == "anonymous":
            return queryset.filter(customer__isnull=True)

        if value.isdigit():
            return queryset.filter(customer__id=int(value))

        return queryset

    class Meta:
        model = Sale
        fields = [
            "state",
            "payment_method",
            "customer_id",
            "date_from",
            "date_to",
        ]


class SaleAdminFilter(SaleFilter):
    user_id = django_filters.NumberFilter(field_name="user__id")
    updated_by = django_filters.NumberFilter(field_name="updated_by")
    deleted_by = django_filters.NumberFilter(field_name="deleted_by")

    is_updated = django_filters.BooleanFilter(method="filter_is_updated")
    is_deleted = django_filters.BooleanFilter(method="filter_is_deleted")

    def filter_is_updated(self, queryset, name, value):
        return queryset.filter(updated_at__isnull=not value)

    def filter_is_deleted(self, queryset, name, value):
        return queryset.filter(deleted_at__isnull=not value)

    class Meta(SaleFilter.Meta):
        pass
