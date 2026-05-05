from typing import ClassVar

from django.db import models
from rest_framework.exceptions import NotFound


class NestedDetailMixin:
    """
    Mixin para ViewSets de detalles anidados.

    Las subclases deben definir:
        parent_model: El modelo padre (ej: Sale, Purchase)
        parent_lookup_kwarg: El kwarg del padre en kwargs (ej: 'sales_pk')
        detail_model: El modelo del detalle (ej: SaleDetail)
        detail_select_related: Tupla de relaciones para select_related
        detail_filter_field: El campo de filtrado (ej: 'sale__id')
        ordering: Orden por defecto (ej: 'created_at')
        not_found_msg: Mensaje si el padre no existe
    """

    parent_model: ClassVar[type[models.Model] | None] = None
    parent_lookup_kwarg: ClassVar[str | None] = None
    detail_model: ClassVar[type[models.Model] | None] = None
    detail_select_related: ClassVar[tuple[str, ...]] = ()
    detail_filter_field: ClassVar[str | None] = None
    ordering: ClassVar[str] = "created_at"
    not_found_msg: ClassVar[str | None] = None

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return self.detail_model.objects.none()

        parent_pk = self.kwargs.get(self.parent_lookup_kwarg)
        if not self.parent_model.objects.filter(pk=parent_pk).exists():
            raise NotFound(
                self.not_found_msg
                or f"{self.parent_model.__name__} {parent_pk} not found."
            )

        qs = (
            self.detail_model.objects.select_related(*self.detail_select_related)
            .filter(**{self.detail_filter_field: parent_pk})
            .order_by(self.ordering)
        )
        return qs
