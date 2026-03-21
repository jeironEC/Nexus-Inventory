# Internal

# Django
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db import IntegrityError
from django.db.models import Sum, Count, Avg, Q

# DRF
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import NotFound

# DRF Spectacular
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

# Serializers
from .serializers.empty import EmptySerializer
from .serializers.user_role import RoleSerializer
from .serializers.user_read import UserReadSerializer
from .serializers.user_create import UserCreateSerializer
from .serializers.user_update import UserUpdateSerializer
from .serializers.token_pair import EmailTokenObtainPairSerializer
from .serializers.category import CategorySerializer
from .serializers.product import ProductSerializer
from .serializers.inventory import InventorySerializer
from .serializers.inventory_movement import InventoryMovementSerializer
from .serializers.customer import CustomerSerializer
from .serializers.promotion import PromotionSerializer
from .serializers.customer_promotion import CustomerPromotionSerializer
from .serializers.sale_read import SaleReadSerializer
from .serializers.sale_create import SaleCreateSerializer
from .serializers.sale_detail_read import SaleDetailReadSerializer
from .serializers.invoice import InvoiceSerializer
from .serializers.supplier import SupplierSerializer
from .serializers.purchase_read import PurchaseReadSerializer
from .serializers.purchase_create import PurchaseCreateSerializer
from .serializers.purchase_detail_read import PurchaseDetailReadSerializer
from .serializers.reports import (
    SaleReportSerializer,
    SaleByCustomerSerializer,
    SaleByPaymentMethodSerializer,
    SaleByPeriodSerializer,
    PurchaseReportSerializer,
    PurchaseBySupplierSerializer,
    PurchaseByPeriodSerializer,
    InventoryReportSerializer,
    InventoryLowStockSerializer,
    InventoryMovementReportSerializer,
    ProductTopSellingSerializer,
    ProductLowSellingSerializer,
    ProductMostPurchasedSerializer,
    ProductByCategorySerializer,
    CustomerTopSerializer,
    CustomerPromotionReportSerializer,
    InvoiceReportSerializer,
)

# Filters
from .filters.user_role import RoleAdminFilter, RoleFilter
from .filters.user import UserAdminFilter, UserFilter
from .filters.category import CategoryAdminFilter, CategoryFilter
from .filters.product import ProductAdminFilter, ProductFilter
from .filters.inventory import InventoryAdminFilter, InventoryFilter
from .filters.inventory_movements import (
    InventoryMovementAdminFilter,
    InventoryMovementFilter,
)
from .filters.customer import CustomerAdminFilter, CustomerFilter
from .filters.promotion import PromotionAdminFilter, PromotionFilter
from .filters.customer_promotions import (
    CustomerPromotionAdminFilter,
    CustomerPromotionFilter,
)
from .filters.sale import (
    SaleAdminFilter,
    SaleFilter,
)
from .filters.sale_detail import (
    SaleDetailAdminFilter,
    SaleDetailFilter,
)
from .filters.invoice import (
    InvoiceAdminFilter,
    InvoiceFilter,
)
from .filters.supplier import (
    SupplierAdminFilter,
    SupplierFilter,
)
from .filters.purchase import (
    PurchaseAdminFilter,
    PurchaseFilter,
)
from .filters.purchase_detail import (
    PurchaseDetailAdminFilter,
    PurchaseDetailFilter,
)
from .filters.reports import (
    SaleReportFilter,
    PurchaseReportFilter,
    InventoryReportFilter,
    ProductReportFilter,
    CustomerReportFilter,
    InvoiceReportFilter,
)

# Models
from nexus_inventory_backend.db.models import (
    Role,
    User,
    Category,
    Product,
    Inventory,
    InventoryMovement,
    Customer,
    Promotion,
    CustomerPromotion,
    Sale,
    SaleDetail,
    Invoice,
    Supplier,
    Purchase,
    PurchaseDetail,
)

# Permissions
from .permissions import CanCreateUsers

# Mixins
from .mixins.filter import StrictFilterMixin
from .mixins.state import StateMixin
from .mixins.noput import NoPutMixin
from .mixins.role_filter import RoleFilterMixin
from .mixins.soft_delete_queryset import SoftDeleteQuerysetMixin
from .mixins.operation_state import OperationStateMixin
from .mixins.report_filter import ReportFilterMixin

# Enums
from nexus_inventory_backend.db.enums import OperationState, InvoiceState

# Utils
from api.utils import get_trunc_func


def healthcheck(request):
    """
    Muestra el estado de la API
    """
    return JsonResponse({"health": "ok"}, status=200)


class UserRoleViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona los roles de usuario del sistema.
    Solo los administradores pueden gestionar todo el sistema.
    """

    queryset = (
        Role.objects.select_related("created_by", "updated_by", "deleted_by")
        .all()
        .order_by("name")
    )
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = RoleAdminFilter
    user_filterset_class = RoleFilter


class UserViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Gestiona los usuarios del sistema.
    Solo permite creación y listado. La edición y eliminación se hace desde /me.
    """

    queryset = (
        User.objects.select_related("created_by", "updated_by", "deleted_by")
        .filter(deleted_at__isnull=True)
        .order_by("created_at")
    )
    permission_classes = [IsAuthenticated, CanCreateUsers]
    admin_filterset_class = UserAdminFilter
    user_filterset_class = UserFilter

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserReadSerializer


class UserMeViewSet(SoftDeleteQuerysetMixin, viewsets.GenericViewSet):
    """
    Expone el perfil del usuario autenticado.
    Permite consultar, actualizar parcialmente y eliminar (soft delete) su propia cuenta.
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UserUpdateSerializer
        return UserReadSerializer

    @action(
        detail=False, methods=["get", "patch", "delete"], url_path="me", url_name="me"
    )
    def me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer_class()(request.user)
            return Response(serializer.data)

        if request.method == "PATCH":
            serializer = self.get_serializer_class()(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        if request.method == "DELETE":
            request.user.soft_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class EmailTokenObtainPairViewSet(TokenObtainPairView):
    """
    Autenticación mediante email y contraseña.
    Retorna un par de tokens JWT (access y refresh).
    """

    serializer_class = EmailTokenObtainPairSerializer


class CategoryViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona las categorías de productos.
    Permite activar y desactivar categorías mediante los endpoints /activate y /deactivate.
    """

    queryset = (
        Category.objects.select_related("created_by", "updated_by", "deleted_by")
        .all()
        .order_by("name")
    )
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = CategoryAdminFilter
    user_filterset_class = CategoryFilter


class ProductViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona los productos del sistema.
    Permite activar y desactivar productos mediante los endpoints /activate y /deactivate.
    """

    queryset = (
        Product.objects.select_related(
            "category", "created_by", "updated_by", "deleted_by"
        )
        .all()
        .order_by("name")
    )
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = ProductAdminFilter
    user_filterset_class = ProductFilter


class InventoryViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    SoftDeleteQuerysetMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Expone el inventario actual de productos en modo lectura.
    Incluye endpoints para consultar por producto y detectar stock bajo.
    """

    queryset = (
        Inventory.objects.select_related(
            "product", "created_by", "updated_by", "deleted_by"
        )
        .all()
        .order_by("product__name")
    )
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = InventoryAdminFilter
    user_filterset_class = InventoryFilter

    @action(detail=False, methods=["get"], url_path=r"product/(?P<product_id>\d+)")
    def get_by_product(self, request, product_id=None):
        inventory = get_object_or_404(self.get_queryset(), product_id=product_id)
        serializer = self.get_serializer(inventory)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="low-stock")
    def low_stock(self, request):
        inventory = self.get_queryset().filter(
            quantity__lte=settings.LOW_STOCK_THRESHOLD
        )
        serializer = self.get_serializer(inventory, many=True)
        return Response(serializer.data)


class InventoryMovementViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Expone los movimientos de inventario en modo lectura.
    Los movimientos son generados por el sistema, no se crean ni modifican manualmente.
    """

    queryset = (
        InventoryMovement.objects.select_related("product", "user")
        .all()
        .order_by("-created_at")
    )
    serializer_class = InventoryMovementSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = InventoryMovementAdminFilter
    user_filterset_class = InventoryMovementFilter


class CustomerViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona los clientes del sistema.
    Permite consultar las promociones asignadas a un cliente específico.
    """

    queryset = (
        Customer.objects.select_related("created_by", "updated_by", "deleted_by")
        .all()
        .order_by("first_name")
    )
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = CustomerAdminFilter
    user_filterset_class = CustomerFilter

    @action(
        detail=True,
        methods=["get"],
        url_path="list-promotions",
    )
    def list_promotions(self, request, pk=None):
        customer = self.get_object()

        promotions = CustomerPromotion.objects.filter(customer=customer).select_related(
            "promotion"
        )

        serializer = CustomerPromotionSerializer(promotions, many=True)
        return Response(serializer.data)


class PromotionViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona las promociones del sistema.
    """

    queryset = (
        Promotion.objects.select_related("created_by", "updated_by", "deleted_by")
        .all()
        .order_by("name")
    )
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = PromotionAdminFilter
    user_filterset_class = PromotionFilter


class CustomerPromotionViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    NoPutMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona la asignación de promociones a clientes.
    Evita duplicados: si la promoción ya está asignada retorna 400.
    """

    queryset = (
        CustomerPromotion.objects.select_related(
            "customer", "promotion", "created_by", "updated_by", "deleted_by"
        )
        .all()
        .order_by("customer__first_name", "promotion__name")
    )
    serializer_class = CustomerPromotionSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = CustomerPromotionAdminFilter
    user_filterset_class = CustomerPromotionFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except IntegrityError:
            return Response(
                {"detail": "This promotion is already assigned to the customer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class SaleViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    OperationStateMixin,
    NoPutMixin,
    SoftDeleteQuerysetMixin,
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

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return SaleCreateSerializer
        if self.action == "cancel":
            return EmptySerializer
        return SaleReadSerializer

    @action(
        detail=True,
        methods=["patch"],
        url_name="cancel",
        serializer_class=EmptySerializer,
    )
    def cancel(self, request, pk=None):
        sale = self.get_object()

        if sale.state == OperationState.CANCELED:
            return Response(
                {"detail": "Sale is already canceled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sale.state = OperationState.CANCELED
        sale.updated_by = request.user
        sale.save(update_fields=["state", "updated_by", "updated_at"])

        serializer = SaleReadSerializer(sale, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    viewsets.ModelViewSet,
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

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return SaleDetail.objects.none()

        sale_pk = self.kwargs.get("sales_pk")
        if not Sale.objects.filter(pk=sale_pk).exists():
            raise NotFound(f"Sale {sale_pk} not found.")

        return (
            SaleDetail.objects.select_related(
                "product",
                "product__category",
                "inventory_movement",
            )
            .filter(sale__id=sale_pk)
            .order_by("created_at")
        )


class InvoiceViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ReadOnlyModelViewSet,
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

    queryset = (
        Invoice.objects.select_related(
            "sale",
            "sale__customer",
            "sale__user",
            "sale__updated_by",
            "sale__deleted_by",
        )
        .all()
        .order_by("-created_at")
    )

    def get_serializer_class(self):
        if self.action == "cancel":
            return EmptySerializer
        return InvoiceSerializer

    @action(
        detail=True,
        methods=["patch"],
        url_name="cancel",
        serializer_class=EmptySerializer,
    )
    def cancel(self, request, pk=None):
        invoice = self.get_object()

        if invoice.state == InvoiceState.CANCELED:
            return Response(
                {"detail": "Invoice is already canceled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invoice.state = InvoiceState.CANCELED
        invoice.updated_by = request.user
        invoice.save(update_fields=["state", "updated_by", "updated_at"])

        serializer = InvoiceSerializer(invoice, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SupplierViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona los suplidores del sistema.
    """

    queryset = (
        Supplier.objects.select_related("created_by", "updated_by", "deleted_by")
        .all()
        .order_by("name")
    )
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = SupplierAdminFilter
    user_filterset_class = SupplierFilter


class PurchaseViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    OperationStateMixin,
    NoPutMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona las compras del sistema.
    Permite cancelar compras mediante el endpoint /cancel.
    """

    permission_classes = [IsAuthenticated]
    admin_filterset_class = PurchaseAdminFilter
    user_filterset_class = PurchaseFilter

    queryset = (
        Purchase.objects.select_related(
            "supplier",
            "user",
            "updated_by",
            "deleted_by",
        )
        .all()
        .order_by("-created_at")
    )

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return PurchaseCreateSerializer
        if self.action == "cancel":
            return EmptySerializer
        return PurchaseReadSerializer

    @action(
        detail=True,
        methods=["patch"],
        url_name="cancel",
        serializer_class=EmptySerializer,
    )
    def cancel(self, request, pk=None):
        purchase = self.get_object()

        if purchase.state == OperationState.CANCELED:
            return Response(
                {"detail": "Purchase is already canceled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        purchase.state = OperationState.CANCELED
        purchase.updated_by = request.user
        purchase.save(update_fields=["state", "updated_by", "updated_at"])

        serializer = PurchaseReadSerializer(purchase, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="purchases_pk", type=int, location=OpenApiParameter.PATH
            )
        ]
    ),
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter(
                name="purchases_pk", type=int, location=OpenApiParameter.PATH
            )
        ]
    ),
)
class PurchaseDetailViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona los detalles de una compra.
    Al crear un detalle se genera automáticamente un InventoryMovement de tipo 'in'.
    """

    serializer_class = PurchaseDetailReadSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = PurchaseDetailAdminFilter
    user_filterset_class = PurchaseDetailFilter
    http_method_names = ["get"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return PurchaseDetail.objects.none()

        purchase_pk = self.kwargs.get("purchases_pk")
        if not Purchase.objects.filter(pk=purchase_pk).exists():
            raise NotFound(f"Purchase {purchase_pk} not found.")

        return (
            PurchaseDetail.objects.select_related(
                "product",
                "product__category",
                "inventory_movement",
            )
            .filter(purchase__id=purchase_pk)
            .order_by("created_at")
        )


class SaleReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las ventas del sistema.
    Incluye resumen general, agrupación por cliente, método de pago y periodo (day, week, month).
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=SaleReportSerializer)
    @action(detail=False, methods=["get"], url_path="sales")
    def sales(self, request):
        qs = self.get_filtered_queryset(Sale.objects.all(), SaleReportFilter)
        data = qs.aggregate(
            total_sales=Count("id", filter=Q(state=OperationState.COMPLETED)),
            total_revenue=Sum("total_amount", filter=Q(state=OperationState.COMPLETED)),
            total_tax=Sum("tax_amount", filter=Q(state=OperationState.COMPLETED)),
            average_ticket=Avg(
                "total_amount", filter=Q(state=OperationState.COMPLETED)
            ),
            canceled_sales=Count("id", filter=Q(state=OperationState.CANCELED)),
        )
        serializer = SaleReportSerializer(data)
        return Response(serializer.data)

    @extend_schema(responses=SaleByCustomerSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="sales/by-customer")
    def sales_by_customer(self, request):
        qs = self.get_filtered_queryset(
            Sale.objects.filter(state=OperationState.COMPLETED), SaleReportFilter
        )
        data = (
            qs.values("customer__id", "customer__first_name", "customer__last_name")
            .annotate(total_sales=Count("id"), total_revenue=Sum("total_amount"))
            .order_by("-total_revenue")
        )
        result = [
            {
                "customer_id": r["customer__id"],
                "customer_name": f"{r['customer__first_name'] or ''} {r['customer__last_name'] or ''}".strip()
                or "Anonymous",
                "total_sales": r["total_sales"],
                "total_revenue": r["total_revenue"],
            }
            for r in data
        ]
        serializer = SaleByCustomerSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=SaleByPaymentMethodSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="sales/by-payment-method")
    def sales_by_payment_method(self, request):
        qs = self.get_filtered_queryset(
            Sale.objects.filter(state=OperationState.COMPLETED), SaleReportFilter
        )
        data = (
            qs.values("payment_method")
            .annotate(total_sales=Count("id"), total_revenue=Sum("total_amount"))
            .order_by("-total_revenue")
        )
        result = [
            {
                "payment_method": r["payment_method"],
                "total_sales": r["total_sales"],
                "total_revenue": r["total_revenue"],
            }
            for r in data
        ]
        serializer = SaleByPaymentMethodSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=SaleByPeriodSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="sales/by-period")
    def sales_by_period(self, request):
        period = request.query_params.get("period", "month")
        trunc_func = get_trunc_func(period)
        qs = self.get_filtered_queryset(
            Sale.objects.filter(state=OperationState.COMPLETED), SaleReportFilter
        )
        data = (
            qs.annotate(period=trunc_func("created_at"))
            .values("period")
            .annotate(total_sales=Count("id"), total_revenue=Sum("total_amount"))
            .order_by("period")
        )
        result = [
            {
                "period": r["period"].strftime("%Y-%m-%d") if r["period"] else None,
                "total_sales": r["total_sales"],
                "total_revenue": r["total_revenue"],
            }
            for r in data
        ]
        serializer = SaleByPeriodSerializer(result, many=True)
        return Response(serializer.data)


class PurchaseReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las compras del sistema.
    Incluye resumen general, agrupación por proveedor y periodo (day, week, month).
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=PurchaseReportSerializer)
    @action(detail=False, methods=["get"], url_path="purchases")
    def purchases(self, request):
        qs = self.get_filtered_queryset(Purchase.objects.all(), PurchaseReportFilter)
        data = qs.aggregate(
            total_purchases=Count("id", filter=Q(state=OperationState.COMPLETED)),
            total_spent=Sum("total_amount", filter=Q(state=OperationState.COMPLETED)),
            average_purchase=Avg(
                "total_amount", filter=Q(state=OperationState.COMPLETED)
            ),
            canceled_purchases=Count("id", filter=Q(state=OperationState.CANCELED)),
        )
        serializer = PurchaseReportSerializer(data)
        return Response(serializer.data)

    @extend_schema(responses=PurchaseBySupplierSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="purchases/by-supplier")
    def purchases_by_supplier(self, request):
        qs = self.get_filtered_queryset(
            Purchase.objects.filter(state=OperationState.COMPLETED),
            PurchaseReportFilter,
        )
        data = (
            qs.values("supplier__id", "supplier__name")
            .annotate(total_purchases=Count("id"), total_spent=Sum("total_amount"))
            .order_by("-total_spent")
        )
        result = [
            {
                "supplier_id": r["supplier__id"],
                "supplier_name": r["supplier__name"],
                "total_purchases": r["total_purchases"],
                "total_spent": r["total_spent"],
            }
            for r in data
        ]
        serializer = PurchaseBySupplierSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=PurchaseByPeriodSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="purchases/by-period")
    def purchases_by_period(self, request):
        period = request.query_params.get("period", "month")
        trunc_func = get_trunc_func(period)
        qs = self.get_filtered_queryset(
            Purchase.objects.filter(state=OperationState.COMPLETED),
            PurchaseReportFilter,
        )
        data = (
            qs.annotate(period=trunc_func("created_at"))
            .values("period")
            .annotate(total_purchases=Count("id"), total_spent=Sum("total_amount"))
            .order_by("period")
        )
        result = [
            {
                "period": r["period"].strftime("%Y-%m-%d") if r["period"] else None,
                "total_purchases": r["total_purchases"],
                "total_spent": r["total_spent"],
            }
            for r in data
        ]
        serializer = PurchaseByPeriodSerializer(result, many=True)
        return Response(serializer.data)


class InventoryReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con el inventario del sistema.
    Incluye stock actual por producto, productos con stock bajo un umbral configurable
    y historial de movimientos de inventario (entradas y salidas).
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=InventoryReportSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="inventory")
    def inventory(self, request):
        qs = self.get_filtered_queryset(
            Inventory.objects.select_related("product", "product__category").all(),
            InventoryReportFilter,
        )
        result = [
            {
                "product_id": inv.product.id,
                "product_name": inv.product.name,
                "category": inv.product.category.name,
                "quantity": inv.quantity,
                "sale_price": inv.product.sale_price,
                "stock_value": inv.quantity * inv.product.sale_price,
            }
            for inv in qs
        ]
        serializer = InventoryReportSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=InventoryLowStockSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="inventory/low-stock")
    def low_stock(self, request):
        threshold = int(
            request.query_params.get(
                "low_stock_threshold", settings.LOW_STOCK_THRESHOLD
            )
        )
        qs = self.get_filtered_queryset(
            Inventory.objects.select_related("product", "product__category").filter(
                quantity__lte=threshold
            ),
            InventoryReportFilter,
        )
        result = [
            {
                "product_id": inv.product.id,
                "product_name": inv.product.name,
                "category": inv.product.category.name,
                "quantity": inv.quantity,
                "threshold": threshold,
            }
            for inv in qs
        ]
        serializer = InventoryLowStockSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=InventoryMovementReportSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="inventory/movements")
    def movements(self, request):
        qs = self.get_filtered_queryset(
            InventoryMovement.objects.select_related("product", "user").all(),
            InventoryReportFilter,
        )
        result = [
            {
                "product_id": m.product.id,
                "product_name": m.product.name,
                "movement_type": m.movement_type,
                "quantity": m.quantity,
                "user": (
                    f"{m.user.first_name} {m.user.last_name}" if m.user else "Unknown"
                ),
                "created_at": m.created_at,
            }
            for m in qs
        ]
        serializer = InventoryMovementReportSerializer(result, many=True)
        return Response(serializer.data)


class ProductReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con los productos del sistema.
    Incluye productos más vendidos, menos vendidos, más comprados a proveedores
    y agrupación de ventas por categoría.
    """

    permission_classes = [IsAuthenticated]

    def _base_sale_detail_qs(self):
        return self.get_filtered_queryset(
            SaleDetail.objects.select_related(
                "product", "product__category", "sale"
            ).filter(sale__state=OperationState.COMPLETED),
            ProductReportFilter,
        )

    @extend_schema(responses=ProductTopSellingSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="products/top-selling")
    def top_selling(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        data = (
            self._base_sale_detail_qs()
            .values("product__id", "product__name", "product__category__name")
            .annotate(
                total_quantity_sold=Sum("quantity"), total_revenue=Sum("subtotal")
            )
            .order_by("-total_quantity_sold")[:limit]
        )
        result = [
            {
                "product_id": r["product__id"],
                "product_name": r["product__name"],
                "category": r["product__category__name"],
                "total_quantity_sold": r["total_quantity_sold"],
                "total_revenue": r["total_revenue"],
            }
            for r in data
        ]
        serializer = ProductTopSellingSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=ProductLowSellingSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="products/low-selling")
    def low_selling(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        data = (
            self._base_sale_detail_qs()
            .values("product__id", "product__name", "product__category__name")
            .annotate(
                total_quantity_sold=Sum("quantity"), total_revenue=Sum("subtotal")
            )
            .order_by("total_quantity_sold")[:limit]
        )
        result = [
            {
                "product_id": r["product__id"],
                "product_name": r["product__name"],
                "category": r["product__category__name"],
                "total_quantity_sold": r["total_quantity_sold"],
                "total_revenue": r["total_revenue"],
            }
            for r in data
        ]
        serializer = ProductLowSellingSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=ProductMostPurchasedSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="products/most-purchased")
    def most_purchased(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        qs = self.get_filtered_queryset(
            PurchaseDetail.objects.select_related(
                "product", "product__category", "purchase"
            ).filter(purchase__state=OperationState.COMPLETED),
            ProductReportFilter,
        )
        data = (
            qs.values("product__id", "product__name", "product__category__name")
            .annotate(
                total_quantity_purchased=Sum("quantity"), total_spent=Sum("subtotal")
            )
            .order_by("-total_quantity_purchased")[:limit]
        )
        result = [
            {
                "product_id": r["product__id"],
                "product_name": r["product__name"],
                "category": r["product__category__name"],
                "total_quantity_purchased": r["total_quantity_purchased"],
                "total_spent": r["total_spent"],
            }
            for r in data
        ]
        serializer = ProductMostPurchasedSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=ProductByCategorySerializer(many=True))
    @action(detail=False, methods=["get"], url_path="products/by-category")
    def by_category(self, request):
        data = (
            self._base_sale_detail_qs()
            .values("product__category__id", "product__category__name")
            .annotate(
                total_products=Count("product__id", distinct=True),
                total_quantity_sold=Sum("quantity"),
                total_revenue=Sum("subtotal"),
            )
            .order_by("-total_revenue")
        )
        result = [
            {
                "category_id": r["product__category__id"],
                "category_name": r["product__category__name"],
                "total_products": r["total_products"],
                "total_quantity_sold": r["total_quantity_sold"],
                "total_revenue": r["total_revenue"],
            }
            for r in data
        ]
        serializer = ProductByCategorySerializer(result, many=True)
        return Response(serializer.data)


class CustomerReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con los clientes del sistema.
    Incluye ranking de clientes por gasto total y uso de promociones por cliente.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=CustomerTopSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="customers/top")
    def top_customers(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        qs = self.get_filtered_queryset(
            Customer.objects.filter(sales__state=OperationState.COMPLETED),
            CustomerReportFilter,
        )
        data = (
            qs.values("id", "first_name", "last_name")
            .annotate(
                total_purchases=Count("sales__id", distinct=True),
                total_spent=Sum("sales__total_amount"),
            )
            .order_by("-total_spent")[:limit]
        )
        result = [
            {
                "customer_id": r["id"],
                "customer_name": f"{r['first_name']} {r['last_name']}",
                "total_purchases": r["total_purchases"],
                "total_spent": r["total_spent"],
            }
            for r in data
        ]
        serializer = CustomerTopSerializer(result, many=True)
        return Response(serializer.data)

    @extend_schema(responses=CustomerPromotionReportSerializer(many=True))
    @action(detail=False, methods=["get"], url_path="customers/promotions")
    def customer_promotions(self, request):
        from nexus_inventory_backend.db.models import CustomerPromotion

        qs = self.get_filtered_queryset(
            CustomerPromotion.objects.select_related("customer").all(),
            CustomerReportFilter,
        )
        data = (
            qs.values("customer__id", "customer__first_name", "customer__last_name")
            .annotate(
                total_promotions=Count("id"),
                applied_promotions=Count("id", filter=Q(applied=True)),
            )
            .order_by("-total_promotions")
        )
        result = [
            {
                "customer_id": r["customer__id"],
                "customer_name": f"{r['customer__first_name']} {r['customer__last_name']}",
                "total_promotions": r["total_promotions"],
                "applied_promotions": r["applied_promotions"],
            }
            for r in data
        ]
        serializer = CustomerPromotionReportSerializer(result, many=True)
        return Response(serializer.data)


class InvoiceReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las facturas del sistema.
    Incluye resumen de facturas emitidas, canceladas y con PDF generado.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=InvoiceReportSerializer)
    @action(detail=False, methods=["get"], url_path="invoices")
    def invoices(self, request):
        qs = self.get_filtered_queryset(Invoice.objects.all(), InvoiceReportFilter)
        data = qs.aggregate(
            total_invoices=Count("id"),
            issued_invoices=Count("id", filter=Q(state=InvoiceState.ISSUED)),
            canceled_invoices=Count("id", filter=Q(state=InvoiceState.CANCELED)),
            pdf_generated=Count("id", filter=Q(pdf_generated=True)),
        )
        serializer = InvoiceReportSerializer(data)
        return Response(serializer.data)
