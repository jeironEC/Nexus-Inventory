# Django
import django_filters

# Models
from nexus_inventory_backend.db.models import SaleDetail


class SaleDetailFilter(django_filters.FilterSet):
    product_id = django_filters.NumberFilter(field_name="product__id")
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )

    class Meta:
        model = SaleDetail
        fields = [
            "product_id",
            "date_from",
            "date_to",
        ]


class SaleDetailAdminFilter(SaleDetailFilter):
    class Meta(SaleDetailFilter.Meta):
        pass
