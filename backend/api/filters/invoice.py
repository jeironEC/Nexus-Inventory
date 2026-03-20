# Django
import django_filters

# Models
from nexus_inventory_backend.db.models import Invoice

# Enums
from nexus_inventory_backend.db.enums import InvoiceState


class InvoiceFilter(django_filters.FilterSet):
    state = django_filters.ChoiceFilter(
        field_name="state", choices=InvoiceState.choices
    )
    pdf_generated = django_filters.BooleanFilter(field_name="pdf_generated")
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )

    class Meta:
        model = Invoice
        fields = [
            "state",
            "pdf_generated",
            "date_from",
            "date_to",
        ]


class InvoiceAdminFilter(InvoiceFilter):
    user_id = django_filters.NumberFilter(field_name="user__id")
    updated_by = django_filters.NumberFilter(field_name="updated_by")
    deleted_by = django_filters.NumberFilter(field_name="deleted_by")

    is_updated = django_filters.BooleanFilter(method="filter_is_updated")
    is_deleted = django_filters.BooleanFilter(method="filter_is_deleted")

    def filter_is_updated(self, queryset, name, value):
        return queryset.filter(updated_at__isnull=not value)

    def filter_is_deleted(self, queryset, name, value):
        return queryset.filter(deleted_at__isnull=not value)

    class Meta(InvoiceFilter.Meta):
        pass
