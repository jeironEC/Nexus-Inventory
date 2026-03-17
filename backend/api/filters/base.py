# Django
import django_filters


class AuditFilter(django_filters.FilterSet):
    # Filters
    created_by = django_filters.NumberFilter(field_name="created_by")
    updated_by = django_filters.NumberFilter(field_name="updated_by")
    deleted_by = django_filters.NumberFilter(field_name="deleted_by")

    # Searchs
    is_updated = django_filters.BooleanFilter(method="filter_is_updated")
    is_deleted = django_filters.BooleanFilter(method="filter_is_deleted")

    # Rangs
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )

    def filter_is_updated(self, queryset, name, value):
        return queryset.filter(updated_at__isnull=not value)

    def filter_is_deleted(self, queryset, name, value):
        return queryset.filter(deleted_at__isnull=not value)
