# Django
from django_filters import FilterSet

# DRF
from rest_framework.request import Request

# Internal
from typing import Protocol


class _HasRequest(Protocol):
    request: Request


class RoleFilterMixin:
    admin_filterset_class: type[FilterSet] | None = None
    user_filterset_class: type[FilterSet] | None = None

    def get_filterset_class(self: _HasRequest) -> type[FilterSet] | None:  # type: ignore[override]
        if self.request.user.role.name.lower() == "admin":
            return self.admin_filterset_class  # type: ignore[attr-defined]
        return self.user_filterset_class  # type: ignore[attr-defined]
