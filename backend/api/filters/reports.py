# Django
import django_filters


class SaleReportFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )
    payment_method = django_filters.CharFilter(
        field_name="payment_method", lookup_expr="iexact"
    )
    customer_id = django_filters.NumberFilter(field_name="customer__id")
    period = django_filters.ChoiceFilter(
        choices=[
            ("day", "Day"),
            ("week", "Week"),
            ("month", "Month"),
            ("year", "Year"),
        ],
        method="filter_noop",
    )

    def filter_noop(self, queryset, name, value):
        return queryset


class PurchaseReportFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )
    supplier_id = django_filters.NumberFilter(field_name="supplier__id")
    period = django_filters.ChoiceFilter(
        choices=[
            ("day", "Day"),
            ("week", "Week"),
            ("month", "Month"),
            ("year", "Year"),
        ],
        method="filter_noop",
    )

    def filter_noop(self, queryset, name, value):
        return queryset


class InventoryReportFilter(django_filters.FilterSet):
    category_id = django_filters.NumberFilter(field_name="product__category__id")


class ProductReportFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(
        field_name="sale__created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="sale__created_at__date", lookup_expr="lte"
    )
    category_id = django_filters.NumberFilter(field_name="product__category__id")


class CustomerReportFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(
        field_name="sales__created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="sales__created_at__date", lookup_expr="lte"
    )


class InvoiceReportFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )
    state = django_filters.CharFilter(field_name="state", lookup_expr="iexact")
    invoice_type = django_filters.CharFilter(
        field_name="invoice_type", lookup_expr="iexact"
    )
    sale_id = django_filters.NumberFilter(field_name="sale_id")
    purchase_id = django_filters.NumberFilter(field_name="purchase_id")


class SaleReturnReportFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )
    state = django_filters.CharFilter(field_name="state", lookup_expr="iexact")


class PurchaseReturnReportFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at__date", lookup_expr="lte"
    )
    state = django_filters.CharFilter(field_name="state", lookup_expr="iexact")
