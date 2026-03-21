# DRF
from rest_framework.exceptions import ValidationError


class ReportFilterMixin:
    def get_filtered_queryset(self, queryset, filterset_class):
        filterset = filterset_class(self.request.query_params, queryset=queryset)
        if not filterset.is_valid():
            raise ValidationError(filterset.errors)
        return filterset.qs
