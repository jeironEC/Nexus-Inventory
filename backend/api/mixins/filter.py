# DRF
from rest_framework.exceptions import ValidationError


class StrictFilterMixin:
    def filter_queryset(self, queryset):
        filterset_class = self.get_filterset_class()

        if filterset_class is None:
            return queryset

        filterset = filterset_class(
            self.request.query_params,
            queryset=queryset,
            request=self.request,
        )

        if not filterset.is_valid():
            raise ValidationError(filterset.errors)

        return filterset.qs
