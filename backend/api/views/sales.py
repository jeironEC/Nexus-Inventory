from pathlib import Path
from django.conf import settings
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from nexus_inventory_backend.db.models import (
    Sale,
    SaleDetail,
    Invoice,
)
from nexus_inventory_backend.db.models import Inventory
from nexus_inventory_backend.db.enums import OperationState, InvoiceState, InvoiceType

from api.serializers.empty import EmptySerializer
from api.serializers.sale_read import SaleReadSerializer
from api.serializers.sale_create import SaleCreateSerializer
from api.serializers.sale_detail_read import SaleDetailReadSerializer
from api.serializers.invoice import InvoiceSerializer

from api.filters.sale import SaleAdminFilter, SaleFilter
from api.filters.sale_detail import SaleDetailAdminFilter, SaleDetailFilter
from api.filters.invoice import InvoiceAdminFilter, InvoiceFilter

from api.mixins.filter import StrictFilterMixin
from api.mixins.noput import NoPutMixin
from api.mixins.role_filter import RoleFilterMixin
from api.mixins.soft_delete_queryset import SoftDeleteQuerysetMixin
from api.mixins.audit_fields import AuditOperationUserMixin
from api.mixins.cancelable import CancelableMixin
from api.mixins.nested_detail import NestedDetailMixin

from api.services.company_service import CompanyService


@extend_schema_view(
    list=extend_schema(tags=["Sales"], summary="List sales"),
    create=extend_schema(tags=["Sales"], summary="Create sale"),
    retrieve=extend_schema(tags=["Sales"], summary="Get sale"),
    update=extend_schema(tags=["Sales"], summary="Update sale"),
    partial_update=extend_schema(tags=["Sales"], summary="Partial update sale"),
    destroy=extend_schema(tags=["Sales"], summary="Delete sale"),
    cancel=extend_schema(tags=["Sales"], summary="Cancel sale"),
)
class SaleViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    NoPutMixin,
    AuditOperationUserMixin,
    SoftDeleteQuerysetMixin,
    CancelableMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona las ventas del sistema.
    Permite cancelar ventas mediante el endpoint /cancel.
    """

    permission_classes = [IsAuthenticated]
    admin_filterset_class = SaleAdminFilter
    user_filterset_class = SaleFilter

    queryset = (
        Sale.objects.select_related(
            "customer",
            "user",
            "updated_by",
            "deleted_by",
        )
        .all()
        .order_by("-created_at")
    )

    cancel_state = OperationState.CANCELED
    cancel_already_msg = "Sale is already canceled."

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return SaleCreateSerializer
        if self.action == "cancel":
            return EmptySerializer
        return SaleReadSerializer

    def get_cancel_serializer(self, obj):
        return SaleReadSerializer(obj, context={"request": self.request})

    def on_cancel(self, obj):
        for detail in obj.details.select_related("product"):
            try:
                inventory = Inventory.objects.get(product=detail.product)
                inventory.quantity += detail.quantity
                inventory.save()
            except Inventory.DoesNotExist:
                pass


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(name="sales_pk", type=int, location=OpenApiParameter.PATH)
        ]
    ),
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter(name="sales_pk", type=int, location=OpenApiParameter.PATH)
        ]
    ),
)
class SaleDetailViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    NestedDetailMixin,
    ListModelMixin,
    RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Gestiona los detalles de una venta.
    Al crear un detalle se genera automáticamente un InventoryMovement de tipo 'out' y su respectiva factura.
    """

    serializer_class = SaleDetailReadSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = SaleDetailAdminFilter
    user_filterset_class = SaleDetailFilter
    http_method_names = ["get"]

    parent_model = Sale
    parent_lookup_kwarg = "sales_pk"
    detail_model = SaleDetail
    detail_select_related = ("product", "product__category", "inventory_movement")
    detail_filter_field = "sale__id"
    ordering = "created_at"
    not_found_msg = None


@extend_schema_view(
    list=extend_schema(tags=["Invoices"], summary="List invoices"),
    retrieve=extend_schema(tags=["Invoices"], summary="Get invoice"),
    cancel=extend_schema(tags=["Invoices"], summary="Cancel invoice"),
)
class InvoiceViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    SoftDeleteQuerysetMixin,
    CancelableMixin,
    ListModelMixin,
    RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Gestiona las facturas del sistema.
    Las facturas se generan automáticamente al crear una venta.
    Permite cancelar facturas mediante el endpoint /cancel.
    """

    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = InvoiceAdminFilter
    user_filterset_class = InvoiceFilter

    cancel_state = InvoiceState.CANCELED
    cancel_already_msg = "Invoice is already canceled."

    def get_queryset(self):
        return (
            Invoice.objects.select_related(
                "sale",
                "sale__customer",
                "sale__user",
                "sale__updated_by",
                "sale__deleted_by",
                "purchase",
                "purchase__supplier",
                "purchase__user",
            )
            .all()
            .order_by("-created_at")
        )

    def get_serializer_class(self):
        if self.action == "cancel":
            return EmptySerializer
        return InvoiceSerializer

    def get_cancel_serializer(self, obj):
        return InvoiceSerializer(obj, context={"request": self.request})

    @action(
        detail=True,
        methods=["get"],
        url_name="pdf",
        url_path="pdf",
        serializer_class=EmptySerializer,
    )
    def pdf(self, request, pk=None):
        invoice = self.get_object()

        company = CompanyService.get_active_company()

        template = (
            "pdf/invoice_sale.html"
            if invoice.invoice_type == InvoiceType.SALE.value
            else "pdf/invoice_purchase.html"
        )

        html_content = render_to_string(
            template,
            {
                "invoice": invoice,
                "company": company,
            },
        )

        pdf_file = HTML(
            string=html_content,
            base_url=str(Path(settings.MEDIA_ROOT) / ""),
        ).write_pdf()

        invoice.pdf_generated = True
        invoice.save(update_fields=["pdf_generated", "updated_at"])

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="factura_{invoice.number_invoice}.pdf"'
        )

        return response
