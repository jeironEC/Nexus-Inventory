from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from nexus_inventory_backend.db.models import (
    SaleReturn,
    SaleReturnDetail,
    PurchaseReturn,
    PurchaseReturnDetail,
)
from nexus_inventory_backend.db.enums import OperationState

from api.serializers.empty import EmptySerializer
from api.serializers.sale_return_read import SaleReturnReadSerializer
from api.serializers.sale_return_create import SaleReturnCreateSerializer
from api.serializers.sale_return_detail_read import SaleReturnDetailReadSerializer
from api.serializers.purchase_return_read import PurchaseReturnReadSerializer
from api.serializers.purchase_return_create import PurchaseReturnCreateSerializer
from api.serializers.purchase_return_detail_read import (
    PurchaseReturnDetailReadSerializer,
)

from api.services.operation_service import (
    cancel_sale_return,
    cancel_purchase_return,
)

from api.filters.sale_return import SaleReturnAdminFilter, SaleReturnFilter
from api.filters.sale_return_detail import (
    SaleReturnDetailAdminFilter,
    SaleReturnDetailFilter,
)
from api.filters.purchase_return import PurchaseReturnAdminFilter, PurchaseReturnFilter
from api.filters.purchase_return_detail import (
    PurchaseReturnDetailAdminFilter,
    PurchaseReturnDetailFilter,
)

from api.mixins.filter import StrictFilterMixin
from api.mixins.noput import NoPutMixin
from api.mixins.role_filter import RoleFilterMixin
from api.mixins.soft_delete_queryset import SoftDeleteQuerysetMixin
from api.mixins.audit_fields import AuditOperationUserMixin
from api.mixins.cancelable import CancelableMixin
from api.mixins.nested_detail import NestedDetailMixin


@extend_schema_view(
    list=extend_schema(tags=["Sale Returns"], summary="List sale returns"),
    create=extend_schema(tags=["Sale Returns"], summary="Create sale return"),
    retrieve=extend_schema(tags=["Sale Returns"], summary="Get sale return"),
    partial_update=extend_schema(
        tags=["Sale Returns"], summary="Partial update sale return"
    ),
    destroy=extend_schema(tags=["Sale Returns"], summary="Delete sale return"),
    cancel=extend_schema(tags=["Sale Returns"], summary="Cancel sale return"),
)
class SaleReturnViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    NoPutMixin,
    AuditOperationUserMixin,
    SoftDeleteQuerysetMixin,
    CancelableMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona las devoluciones de ventas del sistema.
    Permite cancelar devoluciones mediante el endpoint /cancel.
    """

    permission_classes = [IsAuthenticated]
    admin_filterset_class = SaleReturnAdminFilter
    user_filterset_class = SaleReturnFilter

    queryset = (
        SaleReturn.objects.select_related(
            "sale",
            "sale__customer",
            "user",
            "updated_by",
            "deleted_by",
        )
        .all()
        .order_by("-created_at")
    )

    cancel_state = OperationState.CANCELED
    cancel_already_msg = "Sale return is already canceled."

    def on_cancel(self, obj):
        cancel_sale_return(obj)

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return SaleReturnCreateSerializer
        if self.action == "cancel":
            return EmptySerializer
        return SaleReturnReadSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "create":
            context["sale"] = self.request.data.get("sale") or self.request.data.get(
                "sale_id"
            )
        return context

    def get_cancel_serializer(self, obj):
        return SaleReturnReadSerializer(obj, context={"request": self.request})


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="sale_returns_pk", type=int, location=OpenApiParameter.PATH
            )
        ]
    ),
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter(
                name="sale_returns_pk", type=int, location=OpenApiParameter.PATH
            )
        ]
    ),
)
class SaleReturnDetailViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    NestedDetailMixin,
    ListModelMixin,
    RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Gestiona los detalles de una devolución de venta.
    """

    serializer_class = SaleReturnDetailReadSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = SaleReturnDetailAdminFilter
    user_filterset_class = SaleReturnDetailFilter
    http_method_names = ["get"]

    parent_model = SaleReturn
    parent_lookup_kwarg = "sale_returns_pk"
    detail_model = SaleReturnDetail
    detail_select_related = ("product", "product__category", "inventory_movement")
    detail_filter_field = "sale_return__id"
    ordering = "created_at"
    not_found_msg = None


@extend_schema_view(
    list=extend_schema(tags=["Purchase Returns"], summary="List purchase returns"),
    create=extend_schema(tags=["Purchase Returns"], summary="Create purchase return"),
    retrieve=extend_schema(tags=["Purchase Returns"], summary="Get purchase return"),
    partial_update=extend_schema(
        tags=["Purchase Returns"], summary="Partial update purchase return"
    ),
    destroy=extend_schema(tags=["Purchase Returns"], summary="Delete purchase return"),
    cancel=extend_schema(tags=["Purchase Returns"], summary="Cancel purchase return"),
)
class PurchaseReturnViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    NoPutMixin,
    AuditOperationUserMixin,
    SoftDeleteQuerysetMixin,
    CancelableMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona las devoluciones de compras del sistema.
    Permite cancelar devoluciones mediante el endpoint /cancel.
    """

    permission_classes = [IsAuthenticated]
    admin_filterset_class = PurchaseReturnAdminFilter
    user_filterset_class = PurchaseReturnFilter

    queryset = (
        PurchaseReturn.objects.select_related(
            "purchase",
            "purchase__supplier",
            "user",
            "updated_by",
            "deleted_by",
        )
        .all()
        .order_by("-created_at")
    )

    cancel_state = OperationState.CANCELED
    cancel_already_msg = "Purchase return is already canceled."

    def on_cancel(self, obj):
        cancel_purchase_return(obj)

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return PurchaseReturnCreateSerializer
        if self.action == "cancel":
            return EmptySerializer
        return PurchaseReturnReadSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "create":
            context["purchase"] = self.request.data.get(
                "purchase"
            ) or self.request.data.get("purchase_id")
        return context

    def get_cancel_serializer(self, obj):
        return PurchaseReturnReadSerializer(obj, context={"request": self.request})


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="purchase_returns_pk", type=int, location=OpenApiParameter.PATH
            )
        ]
    ),
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter(
                name="purchase_returns_pk", type=int, location=OpenApiParameter.PATH
            )
        ]
    ),
)
class PurchaseReturnDetailViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    NestedDetailMixin,
    ListModelMixin,
    RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Gestiona los detalles de una devolución de compra.
    """

    serializer_class = PurchaseReturnDetailReadSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = PurchaseReturnDetailAdminFilter
    user_filterset_class = PurchaseReturnDetailFilter
    http_method_names = ["get"]

    parent_model = PurchaseReturn
    parent_lookup_kwarg = "purchase_returns_pk"
    detail_model = PurchaseReturnDetail
    detail_select_related = ("product", "product__category", "inventory_movement")
    detail_filter_field = "purchase_return__id"
    ordering = "created_at"
    not_found_msg = None
