# Internal
import uuid
from hashlib import sha256

# Django
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.http.response import HttpResponse

# Weasyprint
from weasyprint import HTML

# DRF
from rest_framework import mixins, status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import NotFound

# DRF Spectacular
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

# Serializers
from .serializers.empty import EmptySerializer
from .serializers.user_role import RoleSerializer
from .serializers.user_read import UserReadSerializer
from .serializers.password_reset import (
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
    PasswordResetConfirmSerializer,
)
from .serializers.company import CompanySerializer
from .serializers.user_create import UserCreateSerializer
from .serializers.user_update import UserUpdateSerializer
from .serializers.token_pair import EmailTokenObtainPairSerializer
from .serializers.category import CategorySerializer
from .serializers.product import ProductSerializer
from .serializers.inventory import InventorySerializer
from .serializers.inventory_movement import InventoryMovementSerializer
from .serializers.customer import CustomerSerializer
from .serializers.sale_read import SaleReadSerializer
from .serializers.sale_create import SaleCreateSerializer
from .serializers.sale_detail_read import SaleDetailReadSerializer
from .serializers.sale_return_read import SaleReturnReadSerializer
from .serializers.sale_return_create import SaleReturnCreateSerializer
from .serializers.sale_return_detail_read import SaleReturnDetailReadSerializer
from .serializers.invoice import InvoiceSerializer
from .serializers.supplier import SupplierSerializer
from .serializers.purchase_read import PurchaseReadSerializer
from .serializers.purchase_create import PurchaseCreateSerializer
from .serializers.purchase_detail_read import PurchaseDetailReadSerializer
from .serializers.purchase_return_read import PurchaseReturnReadSerializer
from .serializers.purchase_return_create import PurchaseReturnCreateSerializer
from .serializers.purchase_return_detail_read import PurchaseReturnDetailReadSerializer
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
    ProductByCategorySerializer,
    ProductPerformanceSerializer,
    CustomerReportSerializer,
    InvoiceSummarySerializer,
    ReturnReportSummarySerializer,
    ReturnDetailReportSerializer,
)

# Filters
from .filters.user_role import RoleAdminFilter, RoleFilter
from .filters.user import UserAdminFilter, UserFilter
from .filters.company import CompanyAdminFilter, CompanyFilter
from .filters.category import CategoryAdminFilter, CategoryFilter
from .filters.product import ProductAdminFilter, ProductFilter
from .filters.inventory import InventoryAdminFilter, InventoryFilter
from .filters.inventory_movements import (
    InventoryMovementAdminFilter,
    InventoryMovementFilter,
)
from .filters.customer import CustomerAdminFilter, CustomerFilter
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
from .filters.sale_return import (
    SaleReturnAdminFilter,
    SaleReturnFilter,
)
from .filters.sale_return_detail import (
    SaleReturnDetailAdminFilter,
    SaleReturnDetailFilter,
)
from .filters.purchase_return import (
    PurchaseReturnAdminFilter,
    PurchaseReturnFilter,
)
from .filters.purchase_return_detail import (
    PurchaseReturnDetailAdminFilter,
    PurchaseReturnDetailFilter,
)
from .filters.reports import (
    SaleReportFilter,
    PurchaseReportFilter,
    InventoryReportFilter,
    ProductReportFilter,
    CustomerReportFilter,
    InvoiceReportFilter,
    SaleReturnReportFilter,
    PurchaseReturnReportFilter,
)

# Models
from nexus_inventory_backend.db.models import (
    Role,
    User,
    PasswordResetOTP,
    Company,
    Category,
    Product,
    Inventory,
    InventoryMovement,
    Customer,
    Sale,
    SaleDetail,
    Invoice,
    Supplier,
    Purchase,
    PurchaseDetail,
    SaleReturn,
    SaleReturnDetail,
    PurchaseReturn,
    PurchaseReturnDetail,
)

# Permissions
from .permissions import CanCreateUsers

# Mixins
from .mixins.filter import StrictFilterMixin
from .mixins.noput import NoPutMixin
from .mixins.role_filter import RoleFilterMixin
from .mixins.soft_delete_queryset import SoftDeleteQuerysetMixin
from .mixins.report_filter import ReportFilterMixin
from .mixins.audit_fields import AuditUserMixin, AuditOperationUserMixin
from .mixins.is_active import StateMixin

# Enums
from nexus_inventory_backend.db.enums import (
    OperationState,
    InvoiceState,
    InvoiceType,
)

# Services
from api.services.email_service import send_reset_password_email
from api.services.company_service import CompanyService
from api.services.reports.sale_report_service import SaleReportService
from api.services.reports.purchase_report_service import PurchaseReportService
from api.services.reports.inventory_report_service import InventoryReportService
from api.services.reports.product_report_service import ProductReportService
from api.services.reports.customer_report_service import CustomerReportService
from api.services.reports.invoice_report_service import InvoiceReportService
from api.services.reports.sale_return_report_service import SaleReturnReportService
from api.services.reports.purchase_return_report_service import (
    PurchaseReturnReportService,
)
from api.services.util_service import format_currency, generate_otp

# Utils
from api.utils import get_trunc_func

# Date
from datetime import timedelta


@extend_schema(tags=["Health"])
class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes: list[str] = []
    serializer_class = EmptySerializer

    def get(self, request):
        return Response(
            {
                "status": "ok",
                "version": "1.0.0",
                "timestamp": timezone.now().date().isoformat(),
            }
        )


@extend_schema_view(
    list=extend_schema(tags=["Roles"], summary="List roles"),
    create=extend_schema(tags=["Roles"], summary="Create role"),
    retrieve=extend_schema(tags=["Roles"], summary="Get role"),
    partial_update=extend_schema(tags=["Roles"], summary="Partial update role"),
    destroy=extend_schema(tags=["Roles"], summary="Delete role"),
    activate=extend_schema(tags=["Roles"], summary="Activate role"),
    deactivate=extend_schema(tags=["Roles"], summary="Deactivate role"),
)
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

    queryset = Role.objects.all().order_by("name")
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = RoleAdminFilter
    user_filterset_class = RoleFilter


@extend_schema_view(
    list=extend_schema(tags=["Users"], summary="List users"),
    create=extend_schema(tags=["Users"], summary="Create user"),
    activate=extend_schema(tags=["Users"], summary="Activate user"),
    deactivate=extend_schema(tags=["Users"], summary="Deactivate user"),
)
class UserViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    AuditUserMixin,
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


class PasswordResetViewSet(viewsets.ViewSet):
    """
    Recuperación de contraseña mediante email.
    Envia un correo con un código OTP y retorna un mensaje de seguridad.
    Valida el código y retorna un token de recuperación.
    Valida el token y permite cambiar la contraseña.
    """

    def get_serializer_class(self):
        if self.action == "request":
            return PasswordResetRequestSerializer
        elif self.action == "verify":
            return PasswordResetVerifySerializer
        elif self.action == "confirm":
            return PasswordResetConfirmSerializer
        return None

    @action(detail=False, methods=["post"])
    def request(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "If the email address exists, you will receive a code."},
                status=status.HTTP_200_OK,
            )

        if user.role.name.lower() != "admin":
            return Response(
                {"detail": "Only administrators are allowed this action."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        PasswordResetOTP.objects.filter(email=email, is_used=False).update(is_used=True)

        otp = generate_otp()
        otp_hash = sha256(otp.encode()).hexdigest()

        PasswordResetOTP.objects.create(user=user, email=email, otp_hash=otp_hash)

        send_reset_password_email(email, otp, user)

        return Response(
            {"detail": "If the email address exists, you will receive a code."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def verify(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        record = PasswordResetOTP.objects.filter(email=email, is_used=False).first()

        if not record:
            return Response(
                {"detail": "Invalid or expired code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if timezone.now() - record.created_at > timedelta(minutes=5):
            return Response(
                {"detail": "Expired code."}, status=status.HTTP_400_BAD_REQUEST
            )

        if sha256(otp.encode()).hexdigest() != record.otp_hash:
            return Response(
                {"detail": "Invalid code."}, status=status.HTTP_400_BAD_REQUEST
            )

        record.reset_token = uuid.uuid4()
        record.save(update_fields=["reset_token"])

        return Response(
            {"reset_token": str(record.reset_token)}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"])
    def confirm(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_token = serializer.validated_data["reset_token"]
        new_password = serializer.validated_data["new_password"]

        record = PasswordResetOTP.objects.filter(
            reset_token=reset_token, is_used=False
        ).first()

        if not record:
            return Response(
                {"detail": "Invalid or expired reset token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=record.email).first()

        if not user:
            return Response(
                {"detail": "Invalid user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        record.is_used = True
        record.reset_token = None
        record.save(update_fields=["is_used", "reset_token"])

        return Response(
            {"detail": "Password updated successfully"},
            status=status.HTTP_200_OK,
        )


@extend_schema_view(
    list=extend_schema(tags=["Companies"], summary="List companies"),
    create=extend_schema(tags=["Companies"], summary="Create company"),
    retrieve=extend_schema(tags=["Companies"], summary="Get company"),
    partial_update=extend_schema(tags=["Companies"], summary="Partial update company"),
    destroy=extend_schema(tags=["Companies"], summary="Delete company"),
    activate=extend_schema(tags=["Companies"], summary="Activate company"),
    deactivate=extend_schema(tags=["Companies"], summary="Deactivate company"),
)
class CompanyViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    AuditUserMixin,
    SoftDeleteQuerysetMixin,
    viewsets.ModelViewSet,
):
    """
    Gestiona las compañias del sistema.
    Permite activar y desactivar compañias mediante los endpoints /activate y /deactivate.
    """

    queryset = (
        Company.objects.select_related("created_by", "updated_by", "deleted_by")
        .all()
        .order_by("name")
    )
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = CompanyAdminFilter
    user_filterset_class = CompanyFilter


@extend_schema_view(
    list=extend_schema(tags=["Categories"], summary="List categories"),
    create=extend_schema(tags=["Categories"], summary="Create category"),
    retrieve=extend_schema(tags=["Categories"], summary="Get category"),
    partial_update=extend_schema(
        tags=["Categories"], summary="Partial update category"
    ),
    destroy=extend_schema(tags=["Categories"], summary="Delete category"),
    activate=extend_schema(tags=["Categories"], summary="Activate category"),
    deactivate=extend_schema(tags=["Categories"], summary="Deactivate category"),
)
class CategoryViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    AuditUserMixin,
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


@extend_schema_view(
    list=extend_schema(tags=["Products"], summary="List products"),
    create=extend_schema(tags=["Products"], summary="Create product"),
    retrieve=extend_schema(tags=["Products"], summary="Get product"),
    partial_update=extend_schema(tags=["Products"], summary="Partial update product"),
    destroy=extend_schema(tags=["Products"], summary="Delete product"),
    activate=extend_schema(tags=["Products"], summary="Activate product"),
    deactivate=extend_schema(tags=["Products"], summary="Deactivate product"),
)
class ProductViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    AuditUserMixin,
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


@extend_schema_view(
    list=extend_schema(tags=["Inventory"], summary="List inventory"),
    get_by_product=extend_schema(
        tags=["Inventory"], summary="Get inventory by product"
    ),
    low_stock=extend_schema(tags=["Inventory"], summary="List low stock inventory"),
)
class InventoryViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    SoftDeleteQuerysetMixin,
    AuditUserMixin,
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


@extend_schema_view(
    list=extend_schema(
        tags=["Inventory Movements"], summary="List inventory movements"
    ),
    retrieve=extend_schema(
        tags=["Inventory Movements"], summary="Get inventory movement"
    ),
)
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


@extend_schema_view(
    list=extend_schema(tags=["Customers"], summary="List customers"),
    create=extend_schema(tags=["Customers"], summary="Create customer"),
    retrieve=extend_schema(tags=["Customers"], summary="Get customer"),
    partial_update=extend_schema(tags=["Customers"], summary="Partial update customer"),
    destroy=extend_schema(tags=["Customers"], summary="Delete customer"),
    activate=extend_schema(tags=["Customers"], summary="Activate customer"),
    deactivate=extend_schema(tags=["Customers"], summary="Deactivate customer"),
)
class CustomerViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    AuditUserMixin,
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


@extend_schema_view(
    list=extend_schema(tags=["Invoices"], summary="List invoices"),
    retrieve=extend_schema(tags=["Invoices"], summary="Get invoice"),
    cancel=extend_schema(tags=["Invoices"], summary="Cancel invoice"),
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

    @action(
        detail=True,
        methods=["get"],
        url_name="pdf",
        url_path="pdf",
        serializer_class=EmptySerializer,
    )
    def pdf(self, request, pk=None):
        invoice = get_object_or_404(
            Invoice.objects.select_related(
                "sale",
                "sale__customer",
                "sale__user",
                "purchase",
                "purchase__supplier",
                "purchase__user",
            ),
            pk=pk,
        )
        company = CompanyService.get_active_company()

        template = (
            "pdf/invoice_sale.html"
            if invoice.invoice_type == "SALE"
            else "pdf/invoice_purchase.html"
        )

        html_content = render_to_string(
            template,
            {
                "invoice": invoice,
                "company": company,
            },
        )

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="factura_{invoice.number_invoice}.pdf"'
        )

        return response


@extend_schema_view(
    list=extend_schema(tags=["Suppliers"], summary="List suppliers"),
    create=extend_schema(tags=["Suppliers"], summary="Create supplier"),
    retrieve=extend_schema(tags=["Suppliers"], summary="Get supplier"),
    partial_update=extend_schema(tags=["Suppliers"], summary="Partial update supplier"),
    destroy=extend_schema(tags=["Suppliers"], summary="Delete supplier"),
    activate=extend_schema(tags=["Suppliers"], summary="Activate supplier"),
    deactivate=extend_schema(tags=["Suppliers"], summary="Deactivate supplier"),
)
class SupplierViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    StateMixin,
    NoPutMixin,
    AuditUserMixin,
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


@extend_schema_view(
    list=extend_schema(tags=["Purchases"], summary="List purchases"),
    create=extend_schema(tags=["Purchases"], summary="Create purchase"),
    retrieve=extend_schema(tags=["Purchases"], summary="Get purchase"),
    update=extend_schema(tags=["Purchases"], summary="Update purchase"),
    partial_update=extend_schema(tags=["Purchases"], summary="Partial update purchase"),
    destroy=extend_schema(tags=["Purchases"], summary="Delete purchase"),
    cancel=extend_schema(tags=["Purchases"], summary="Cancel purchase"),
)
class PurchaseViewSet(
    StrictFilterMixin,
    RoleFilterMixin,
    NoPutMixin,
    AuditOperationUserMixin,
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

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return SaleReturnCreateSerializer
        if self.action == "cancel":
            return EmptySerializer
        return SaleReturnReadSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "create":
            context["sale_id"] = self.request.data.get("sale_id")
        return context

    @action(
        detail=True,
        methods=["patch"],
        url_name="cancel",
        serializer_class=EmptySerializer,
    )
    def cancel(self, request, pk=None):
        sale_return = self.get_object()

        if sale_return.state == OperationState.CANCELED:
            return Response(
                {"detail": "Sale return is already canceled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sale_return.state = OperationState.CANCELED
        sale_return.updated_by = request.user
        sale_return.save(update_fields=["state", "updated_by", "updated_at"])

        serializer = SaleReturnReadSerializer(sale_return, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    viewsets.ModelViewSet,
):
    """
    Gestiona los detalles de una devolución de venta.
    """

    serializer_class = SaleReturnDetailReadSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = SaleReturnDetailAdminFilter
    user_filterset_class = SaleReturnDetailFilter
    http_method_names = ["get"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return SaleReturnDetail.objects.none()

        sale_return_pk = self.kwargs.get("sale_returns_pk")
        if not SaleReturn.objects.filter(pk=sale_return_pk).exists():
            raise NotFound(f"SaleReturn {sale_return_pk} not found.")

        return (
            SaleReturnDetail.objects.select_related(
                "product",
                "product__category",
                "inventory_movement",
            )
            .filter(sale_return__id=sale_return_pk)
            .order_by("created_at")
        )


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

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return PurchaseReturnCreateSerializer
        if self.action == "cancel":
            return EmptySerializer
        return PurchaseReturnReadSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "create":
            context["purchase_id"] = self.request.data.get("purchase_id")
        return context

    @action(
        detail=True,
        methods=["patch"],
        url_name="cancel",
        serializer_class=EmptySerializer,
    )
    def cancel(self, request, pk=None):
        purchase_return = self.get_object()

        if purchase_return.state == OperationState.CANCELED:
            return Response(
                {"detail": "Purchase return is already canceled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        purchase_return.state = OperationState.CANCELED
        purchase_return.updated_by = request.user
        purchase_return.save(update_fields=["state", "updated_by", "updated_at"])

        serializer = PurchaseReturnReadSerializer(
            purchase_return, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    viewsets.ModelViewSet,
):
    """
    Gestiona los detalles de una devolución de compra.
    """

    serializer_class = PurchaseReturnDetailReadSerializer
    permission_classes = [IsAuthenticated]
    admin_filterset_class = PurchaseReturnDetailAdminFilter
    user_filterset_class = PurchaseReturnDetailFilter
    http_method_names = ["get"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return PurchaseReturnDetail.objects.none()

        purchase_return_pk = self.kwargs.get("purchase_returns_pk")
        if not PurchaseReturn.objects.filter(pk=purchase_return_pk).exists():
            raise NotFound(f"PurchaseReturn {purchase_return_pk} not found.")

        return (
            PurchaseReturnDetail.objects.select_related(
                "product",
                "product__category",
                "inventory_movement",
            )
            .filter(purchase_return__id=purchase_return_pk)
            .order_by("created_at")
        )


class SaleReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las ventas del sistema.
    Utiliza parámetros de consulta para filtrar y agrupar datos.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="group_by",
                type=str,
                enum=["customer", "payment_method", "period"],
                description="Agrupar por...",
            ),
            OpenApiParameter(
                name="period",
                type=str,
                enum=["day", "week", "month", "year"],
                description="Tipo de periodo (solo si group_by=period)",
            ),
        ],
        responses={200: SaleReportSerializer},
    )
    def list(self, request):
        group_by = request.query_params.get("group_by")
        qs = self.get_filtered_queryset(Sale.objects.all(), SaleReportFilter)
        summary = SaleReportService.get_summary(qs)

        if group_by:
            qs_completed = qs.filter(state=OperationState.COMPLETED)
            if group_by == "customer":
                data = SaleReportService.get_by_customer(qs_completed)
                data = SaleByCustomerSerializer(data, many=True).data
            elif group_by == "payment_method":
                data = SaleReportService.get_by_payment_method(qs_completed)
                data = SaleByPaymentMethodSerializer(data, many=True).data
            elif group_by == "period":
                period = request.query_params.get("period", "month")
                trunc_func = get_trunc_func(period)
                data = SaleReportService.get_by_period(qs_completed, trunc_func)
                data = SaleByPeriodSerializer(data, many=True).data
            else:
                data = []
        else:
            # Default: list of sales (now returning summary for the general view)
            serialized_summary = SaleReportSerializer(summary).data
            data = [serialized_summary]

        return Response({"summary": SaleReportSerializer(summary).data, "data": data})

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="group_by", type=str, enum=["customer", "payment_method", "period"]
            ),
            OpenApiParameter(
                name="period", type=str, enum=["day", "week", "month", "year"]
            ),
        ]
    )
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="group_by", type=str, enum=["customer", "payment_method", "period"]
            ),
            OpenApiParameter(
                name="period", type=str, enum=["day", "week", "month", "year"]
            ),
        ]
    )
    @action(detail=False, methods=["get"], url_path="pdf")
    def sales_pdf(self, request):
        group_by = request.query_params.get("group_by")
        company = CompanyService.get_active_company()
        qs = self.get_filtered_queryset(Sale.objects.all(), SaleReportFilter)

        sections = []
        kpis = []

        if group_by:
            if group_by == "customer":
                result = SaleReportService.get_by_customer(qs)
                title = "Ventas por Cliente"
                headers = ["Cliente", "Total Ventas", "Ingresos"]
                data_rows = [
                    {
                        "values_list": [
                            item["customer_name"],
                            item["total_sales"],
                            format_currency(item["total_revenue"]),
                        ]
                    }
                    for item in result
                ]
            elif group_by == "payment_method":
                result = SaleReportService.get_by_payment_method(qs)
                title = "Ventas por Método de Pago"
                headers = ["Método", "Total Ventas", "Ingresos"]
                data_rows = [
                    {
                        "values_list": [
                            item["payment_method_display"],
                            item["total_sales"],
                            format_currency(item["total_revenue"]),
                        ]
                    }
                    for item in result
                ]
            else:  # period
                period = request.query_params.get("period", "month")
                result = SaleReportService.get_by_period(qs, period)
                title = f"Ventas por Período ({period})"
                headers = ["Período", "Total Ventas", "Ingresos"]
                data_rows = [
                    {
                        "values_list": [
                            item["period"],
                            item["total_sales"],
                            format_currency(item["total_revenue"]),
                        ]
                    }
                    for item in result
                ]

            totals = SaleReportService.get_totals_from_list(result)
            kpis = [
                {"label": "Total Ventas", "value": totals["total_sales"]},
                {
                    "label": "Ingresos Totales",
                    "value": format_currency(totals["total_revenue"]),
                    "highlight": True,
                },
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": True}
            )
            filename = "reporte_ventas_agrupado.pdf"
        else:
            data = SaleReportService.build_sales_pdf(qs)
            title = "Reporte Detallado de Ventas"
            headers = [
                "Fecha",
                "Cliente",
                "Método",
                "Subtotal",
                "Impuesto",
                "Total",
                "Estado",
            ]
            data_rows = []
            for sale in data["sales"]:
                data_rows.append(
                    {
                        "values_list": [
                            (
                                sale["created_at"].strftime("%d/%m/%Y")
                                if hasattr(sale["created_at"], "strftime")
                                else sale["created_at"]
                            ),
                            f"{sale.get('customer__first_name', '')} {sale.get('customer__last_name', '')}".strip()
                            or "Anónimo",
                            sale["payment_method"],
                            format_currency(sale["subtotal"]),
                            format_currency(sale["tax_amount"]),
                            format_currency(sale["total_amount"]),
                            {
                                "is_badge": True,
                                "text": (
                                    "Completada"
                                    if sale["state"] == "COMPLETED"
                                    else "Cancelada"
                                ),
                                "badge_type": (
                                    "success"
                                    if sale["state"] == "COMPLETED"
                                    else "danger"
                                ),
                            },
                        ]
                    }
                )

            summary = data["summary"]
            kpis = [
                {"label": "Total Ventas", "value": summary["total_sales"]},
                {
                    "label": "Ingresos",
                    "value": format_currency(summary["total_revenue"]),
                    "highlight": True,
                },
                {"label": "Impuestos", "value": format_currency(summary["total_tax"])},
                {
                    "label": "Ticket Promedio",
                    "value": format_currency(summary["average_ticket"]),
                },
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": False}
            )
            filename = "reporte_ventas_detallado.pdf"

        context = {
            "title": title,
            "company": company,
            "kpis": kpis,
            "sections": sections,
            "now": timezone.now(),
        }

        html_content = render_to_string("pdf/base_report.html", context)
        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{filename}"'
        return response


class PurchaseReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las compras del sistema.
    Utiliza parámetros de consulta para filtrar y agrupar datos.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name="group_by", type=str, enum=["supplier", "period"]),
            OpenApiParameter(
                name="period", type=str, enum=["day", "week", "month", "year"]
            ),
        ],
        responses={200: PurchaseReportSerializer},
    )
    def list(self, request):
        group_by = request.query_params.get("group_by")
        qs = self.get_filtered_queryset(Purchase.objects.all(), PurchaseReportFilter)
        summary = PurchaseReportService.get_summary(qs)

        if group_by:
            qs_completed = qs.filter(state=OperationState.COMPLETED)
            if group_by == "supplier":
                data = PurchaseReportService.get_by_supplier(qs_completed)
                data = PurchaseBySupplierSerializer(data, many=True).data
            elif group_by == "period":
                period = request.query_params.get("period", "month")
                trunc_func = get_trunc_func(period)
                data = PurchaseReportService.get_by_period(qs_completed, trunc_func)
                data = PurchaseByPeriodSerializer(data, many=True).data
            else:
                data = []
        else:
            # Default: Summary for the general view
            serialized_summary = PurchaseReportSerializer(summary).data
            data = [serialized_summary]

        return Response(
            {"summary": PurchaseReportSerializer(summary).data, "data": data}
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(name="group_by", type=str, enum=["supplier", "period"]),
            OpenApiParameter(
                name="period", type=str, enum=["day", "week", "month", "year"]
            ),
        ]
    )
    @action(detail=False, methods=["get"], url_path="pdf")
    def purchases_pdf(self, request):
        group_by = request.query_params.get("group_by")
        company = CompanyService.get_active_company()
        qs = self.get_filtered_queryset(Purchase.objects.all(), PurchaseReportFilter)

        sections = []
        kpis = []

        if group_by:
            if group_by == "supplier":
                result = PurchaseReportService.get_by_supplier(qs)
                title = "Compras por Proveedor"
                headers = ["Proveedor", "Total Compras", "Gasto Total"]
                data_rows = [
                    {
                        "values_list": [
                            item["supplier_name"],
                            item["total_purchases"],
                            format_currency(item["total_spent"]),
                        ]
                    }
                    for item in result
                ]
            else:  # period
                period = request.query_params.get("period", "month")
                result = PurchaseReportService.get_by_period(qs, period)
                title = f"Compras por Período ({period})"
                headers = ["Período", "Total Compras", "Gasto Total"]
                data_rows = [
                    {
                        "values_list": [
                            item["period"],
                            item["total_purchases"],
                            format_currency(item["total_spent"]),
                        ]
                    }
                    for item in result
                ]

            totals = PurchaseReportService.get_totals_from_list(result)
            kpis = [
                {"label": "Total Compras", "value": totals["total_purchases"]},
                {
                    "label": "Gasto Total",
                    "value": format_currency(totals["total_spent"]),
                    "highlight": True,
                },
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": True}
            )
            filename = "reporte_compras_agrupado.pdf"
        else:
            data = PurchaseReportService.build_purchases_pdf(qs)
            title = "Reporte Detallado de Compras"
            headers = ["Fecha", "Proveedor", "Subtotal", "Impuesto", "Total", "Estado"]
            data_rows = []
            for purchase in data["purchases"]:
                data_rows.append(
                    {
                        "values_list": [
                            (
                                purchase["created_at"].strftime("%d/%m/%Y")
                                if hasattr(purchase["created_at"], "strftime")
                                else purchase["created_at"]
                            ),
                            purchase.get("supplier__name", "N/A"),
                            format_currency(purchase["subtotal"]),
                            format_currency(purchase["tax_amount"]),
                            format_currency(purchase["total_amount"]),
                            {
                                "is_badge": True,
                                "text": (
                                    "Completada"
                                    if purchase["state"] == "COMPLETED"
                                    else "Cancelada"
                                ),
                                "badge_type": (
                                    "success"
                                    if purchase["state"] == "COMPLETED"
                                    else "danger"
                                ),
                            },
                        ]
                    }
                )

            summary = data["summary"]
            kpis = [
                {"label": "Total Compras", "value": summary["total_purchases"]},
                {
                    "label": "Gasto Total",
                    "value": format_currency(summary["total_spent"]),
                    "highlight": True,
                },
                {"label": "Impuestos", "value": format_currency(summary["total_tax"])},
                {
                    "label": "Ticket Promedio",
                    "value": format_currency(summary["average_ticket"]),
                },
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": False}
            )
            filename = "reporte_compras_detallado.pdf"

        context = {
            "title": title,
            "company": company,
            "kpis": kpis,
            "sections": sections,
            "now": timezone.now(),
        }

        html_content = render_to_string("pdf/base_report.html", context)
        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{filename}"'
        return response


class InventoryReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con el inventario del sistema.
    Incluye stock actual por producto, productos con stock bajo un umbral configurable
    y historial de movimientos de inventario (entradas y salidas).
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name="view", type=str, enum=["low_stock", "movements"]),
            OpenApiParameter(
                name="low_stock_threshold",
                type=int,
                description="Umbral para stock bajo",
            ),
        ],
        responses={200: InventoryReportSerializer(many=True)},
    )
    def list(self, request):
        view = request.query_params.get("view")

        if view == "low_stock":
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
            raw_data = [
                InventoryReportService.map_low_stock(inv, threshold) for inv in qs
            ]
            summary = InventoryReportService.get_totals_for_inventory(raw_data)
            data = InventoryLowStockSerializer(raw_data, many=True).data
        elif view == "movements":
            qs = self.get_filtered_queryset(
                InventoryMovement.objects.select_related("product", "user").all(),
                InventoryReportFilter,
            )
            raw_data = [InventoryReportService.map_movement(m) for m in qs]
            summary = InventoryReportService.get_totals_for_movements(raw_data)
            data = InventoryMovementReportSerializer(raw_data, many=True).data
        else:
            # Default: Vista general de inventario
            qs = self.get_filtered_queryset(
                Inventory.objects.select_related("product", "product__category").all(),
                InventoryReportFilter,
            )
            raw_data = [InventoryReportService.map_inventory(inv) for inv in qs]
            summary = InventoryReportService.get_totals_for_inventory(raw_data)
            data = InventoryReportSerializer(raw_data, many=True).data

        return Response({"summary": summary, "data": data})

    @extend_schema(
        parameters=[
            OpenApiParameter(name="view", type=str, enum=["low_stock", "movements"]),
            OpenApiParameter(name="low_stock_threshold", type=int),
        ]
    )
    @action(detail=False, methods=["get"], url_path="pdf")
    def inventory_pdf(self, request):
        view = request.query_params.get("view")
        company = CompanyService.get_active_company()
        kpis = []

        if view == "low_stock":
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
                InventoryReportService.map_low_stock(inv, threshold) for inv in qs
            ]
            title = f"Reporte de Bajo Stock (Umbral: {threshold})"
            headers = ["Producto", "Categoría", "Stock Actual", "Umbral", "Estado"]
            data_rows = [
                {
                    "values_list": [
                        item["product_name"],
                        item["category"],
                        item["quantity"],
                        threshold,
                        {
                            "is_badge": True,
                            "text": "Crítico" if item["quantity"] == 0 else "Bajo",
                            "badge_type": (
                                "danger" if item["quantity"] == 0 else "warning"
                            ),
                        },
                    ]
                }
                for item in result
            ]
            kpis = [
                {"label": "Productos Afectados", "value": len(result), "danger": True}
            ]
            filename = "reporte_bajo_stock.pdf"

        elif view == "movements":
            qs = self.get_filtered_queryset(
                InventoryMovement.objects.select_related("product", "user").all(),
                InventoryReportFilter,
            )
            result = [InventoryReportService.map_movement(m) for m in qs]
            totals = InventoryReportService.get_totals_for_movements(result)
            title = "Movimientos de Inventario"
            headers = ["Fecha", "Producto", "Tipo", "Cantidad", "Usuario"]
            data_rows = [
                {
                    "values_list": [
                        item["created_at"],
                        item["product_name"],
                        {
                            "is_badge": True,
                            "text": (
                                "Entrada" if item["movement_type"] == "IN" else "Salida"
                            ),
                            "badge_type": (
                                "success" if item["movement_type"] == "IN" else "info"
                            ),
                        },
                        item["quantity"],
                        item["user"],
                    ]
                }
                for item in result
            ]
            kpis = [
                {"label": "Total Entradas", "value": totals["total_in"]},
                {"label": "Total Salidas", "value": totals["total_out"]},
            ]
            filename = "reporte_movimientos.pdf"

        else:
            qs = self.get_filtered_queryset(
                Inventory.objects.select_related("product", "product__category").all(),
                InventoryReportFilter,
            )
            result = [InventoryReportService.map_inventory(inv) for inv in qs]
            totals = InventoryReportService.get_totals_for_inventory(result)
            title = "Reporte General de Inventario"
            headers = [
                "Producto",
                "Categoría",
                "Cantidad",
                "Precio Venta",
                "Valor Stock",
            ]
            data_rows = [
                {
                    "values_list": [
                        item["product_name"],
                        item["category"],
                        item["quantity"],
                        format_currency(item["sale_price"]),
                        format_currency(item["stock_value"]),
                    ]
                }
                for item in result
            ]
            kpis = [
                {"label": "Total Productos", "value": len(result)},
                {"label": "Stock Total", "value": totals["total_quantity"]},
                {
                    "label": "Valor Total Stock",
                    "value": format_currency(totals["total_stock_value"]),
                    "highlight": True,
                },
            ]
            filename = "reporte_inventario_general.pdf"

        context = {
            "title": title,
            "company": company,
            "kpis": kpis,
            "sections": [
                {"headers": headers, "data": data_rows, "align_last_right": not view}
            ],
            "now": timezone.now(),
        }

        html_content = render_to_string("pdf/base_report.html", context)
        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{filename}"'
        return response


class ProductReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con los productos del sistema.
    Utiliza parámetros de consulta para obtener diferentes vistas.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    def _base_sale_detail_qs(self):
        return self.get_filtered_queryset(
            SaleDetail.objects.select_related(
                "product", "product__category", "sale"
            ).filter(sale__state=OperationState.COMPLETED),
            ProductReportFilter,
        )

    def _base_purchase_detail_qs(self):
        return self.get_filtered_queryset(
            PurchaseDetail.objects.select_related(
                "product", "product__category", "purchase"
            ).filter(purchase__state=OperationState.COMPLETED),
            ProductReportFilter,
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="view",
                type=str,
                enum=["top_selling", "low_selling", "most_purchased", "by_category"],
            ),
            OpenApiParameter(
                name="limit", type=int, description="Límite de resultados"
            ),
        ],
        responses={200: EmptySerializer},
    )
    def list(self, request):
        view = request.query_params.get("view")
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))

        if view == "top_selling":
            data = ProductReportService.get_products_report(
                qs=self._base_sale_detail_qs(), order_by="-total_quantity", limit=limit
            )
            return Response(
                {
                    "summary": {"view": view, "limit": limit},
                    "data": ProductPerformanceSerializer(data, many=True).data,
                }
            )
        elif view == "low_selling":
            data = ProductReportService.get_products_report(
                qs=self._base_sale_detail_qs(), order_by="total_quantity", limit=limit
            )
            return Response(
                {
                    "summary": {"view": view, "limit": limit},
                    "data": ProductPerformanceSerializer(data, many=True).data,
                }
            )
        elif view == "most_purchased":
            data = ProductReportService.get_products_report(
                qs=self._base_purchase_detail_qs(),
                order_by="-total_quantity",
                limit=limit,
            )
            return Response(
                {
                    "summary": {"view": view, "limit": limit},
                    "data": ProductPerformanceSerializer(data, many=True).data,
                }
            )
        elif view == "by_category":
            data = ProductReportService.get_products_by_category(
                self._base_sale_detail_qs()
            )
            return Response(
                {
                    "summary": {"view": view},
                    "data": ProductByCategorySerializer(data, many=True).data,
                }
            )

        # Default: Reporte general
        summary = ProductReportService.build_report_products(
            self._base_sale_detail_qs(), self._base_purchase_detail_qs(), limit
        )
        data = ProductPerformanceSerializer(
            summary.get("top_selling", []), many=True
        ).data

        return Response({"summary": summary, "data": data})

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="view",
                type=str,
                enum=["top_selling", "low_selling", "most_purchased", "by_category"],
            ),
            OpenApiParameter(name="limit", type=int),
        ]
    )
    @action(detail=False, methods=["get"], url_path="pdf")
    def products_pdf(self, request):
        view = request.query_params.get("view")
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        company = CompanyService.get_active_company()
        sections = []
        kpis = []
        title = "Reporte de Productos"

        if view == "top_selling":
            result = ProductReportService.get_products_report(
                qs=self._base_sale_detail_qs(), order_by="-total_quantity", limit=limit
            )
            totals = ProductReportService.get_totals_from_report(result)
            title = "Productos Más Vendidos"
            headers = ["Producto", "Categoría", "Cant. Vendida", "Ingresos"]
            data_rows = [
                {
                    "values_list": [
                        item["product_name"],
                        item["category"],
                        item["total_quantity"],
                        format_currency(item["total_revenue"]),
                    ]
                }
                for item in result
            ]
            kpis = [
                {
                    "label": "Ingresos Totales",
                    "value": format_currency(totals["total_revenue"]),
                    "highlight": True,
                }
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": True}
            )
        elif view == "low_selling":
            result = ProductReportService.get_products_report(
                qs=self._base_sale_detail_qs(), order_by="total_quantity", limit=limit
            )
            totals = ProductReportService.get_totals_from_report(result)
            title = "Productos Menos Vendidos"
            headers = ["Producto", "Categoría", "Cant. Vendida", "Ingresos"]
            data_rows = [
                {
                    "values_list": [
                        item["product_name"],
                        item["category"],
                        item["total_quantity"],
                        format_currency(item["total_revenue"]),
                    ]
                }
                for item in result
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": True}
            )
        elif view == "most_purchased":
            result = ProductReportService.get_products_report(
                qs=self._base_purchase_detail_qs(),
                order_by="-total_quantity",
                limit=limit,
            )
            totals = ProductReportService.get_totals_from_report(
                result, amount_field="total_spent"
            )
            title = "Productos Más Comprados"
            headers = ["Producto", "Categoría", "Cant. Comprada", "Gasto Total"]
            data_rows = [
                {
                    "values_list": [
                        item["product_name"],
                        item["category"],
                        item["total_quantity"],
                        format_currency(item["total_spent"]),
                    ]
                }
                for item in result
            ]
            kpis = [
                {
                    "label": "Gasto Total",
                    "value": format_currency(totals["total_spent"]),
                    "highlight": True,
                }
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": True}
            )
        elif view == "by_category":
            result = ProductReportService.get_products_by_category(
                self._base_sale_detail_qs()
            )
            totals = ProductReportService.get_totals_by_category(result)
            title = "Ventas por Categoría"
            headers = ["Categoría", "Cant. Productos", "Cant. Vendida", "Ingresos"]
            data_rows = [
                {
                    "values_list": [
                        item["category_name"],
                        item["total_products"],
                        item["total_quantity_sold"],
                        format_currency(item["total_revenue"]),
                    ]
                }
                for item in result
            ]
            sections.append(
                {"headers": headers, "data": data_rows, "align_last_right": True}
            )
        else:
            data = ProductReportService.build_report_products(
                self._base_sale_detail_qs(), self._base_purchase_detail_qs(), limit
            )
            title = "Resumen General de Productos"

            # Section: Top Selling
            sections.append(
                {
                    "title": "Top Ventas",
                    "headers": ["Producto", "Cant.", "Ingresos"],
                    "data": [
                        {
                            "values_list": [
                                item["product_name"],
                                item["total_quantity"],
                                format_currency(item["total_revenue"]),
                            ]
                        }
                        for item in data["top_selling"]
                    ],
                    "align_last_right": True,
                }
            )
            # Section: Most Purchased
            sections.append(
                {
                    "title": "Más Comprados",
                    "headers": ["Producto", "Cant.", "Gasto"],
                    "data": [
                        {
                            "values_list": [
                                item["product_name"],
                                item["total_quantity"],
                                format_currency(item["total_spent"]),
                            ]
                        }
                        for item in data["most_purchased"]
                    ],
                    "align_last_right": True,
                }
            )
            kpis = [
                {"label": "Categorías", "value": len(data["by_category"])},
                {
                    "label": "Top Producto",
                    "value": (
                        data["top_selling"][0]["product_name"]
                        if data["top_selling"]
                        else "N/A"
                    ),
                },
            ]

        context = {
            "title": title,
            "company": company,
            "kpis": kpis,
            "sections": sections,
            "now": timezone.now(),
        }

        html_content = render_to_string("pdf/base_report.html", context)
        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reporte_productos.pdf"'
        return response


class CustomerReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con los clientes del sistema.
    Utiliza parámetros de consulta para filtrar y obtener rankings.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name="view", type=str, enum=["top"]),
            OpenApiParameter(
                name="limit", type=int, description="Límite de resultados"
            ),
        ],
        responses={200: CustomerReportSerializer(many=True)},
    )
    def list(self, request):
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        qs = self.get_filtered_queryset(
            Customer.objects.filter(sales__state=OperationState.COMPLETED),
            CustomerReportFilter,
        )
        raw_data = CustomerReportService.get_summary(qs, limit)
        summary = CustomerReportService.get_totals_from_summary(raw_data)
        data = CustomerReportSerializer(raw_data, many=True).data

        return Response({"summary": summary, "data": data})

    @extend_schema(
        parameters=[
            OpenApiParameter(name="view", type=str, enum=["top"]),
            OpenApiParameter(name="limit", type=int),
        ]
    )
    @action(detail=False, methods=["get"], url_path="pdf")
    def customers_pdf(self, request):
        view = request.query_params.get("view")
        limit = int(request.query_params.get("limit", settings.DEFAULT_LIMIT))
        company = CompanyService.get_active_company()
        qs = self.get_filtered_queryset(
            Customer.objects.filter(sales__state=OperationState.COMPLETED),
            CustomerReportFilter,
        )
        result = CustomerReportService.get_summary(qs, limit)
        totals = CustomerReportService.get_totals_from_summary(result)

        title = (
            "Reporte de Clientes Top"
            if view == "top"
            else "Reporte General de Clientes"
        )
        headers = ["Cliente", "Total Compras", "Gasto Total"]
        data_rows = [
            {
                "values_list": [
                    item["customer_name"],
                    item["total_purchases"],
                    format_currency(item["total_spent"]),
                ]
            }
            for item in result
        ]

        kpis = [
            {"label": "Total Clientes", "value": totals["total_customers"]},
            {"label": "Total Compras", "value": totals["total_purchases"]},
            {
                "label": "Gasto Total",
                "value": format_currency(totals["total_spent"]),
                "highlight": True,
            },
        ]

        context = {
            "title": title,
            "company": company,
            "kpis": kpis,
            "sections": [
                {"headers": headers, "data": data_rows, "align_last_right": True}
            ],
            "now": timezone.now(),
        }

        html_content = render_to_string("pdf/base_report.html", context)
        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reporte_clientes.pdf"'
        return response


class InvoiceReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las facturas del sistema.
    Utiliza parámetros de consulta para filtrar por tipo (venta/compra).
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name="type", type=str, enum=["sale", "purchase"]),
        ],
        responses={200: InvoiceSummarySerializer},
    )
    def list(self, request):
        invoice_type = request.query_params.get("type")
        qs = Invoice.objects.all()
        if invoice_type == "sale":
            qs = qs.filter(invoice_type=InvoiceType.SALE)
        elif invoice_type == "purchase":
            qs = qs.filter(invoice_type=InvoiceType.PURCHASE)

        qs_filtered = self.get_filtered_queryset(qs, InvoiceReportFilter)

        if invoice_type == "sale":
            data = InvoiceReportService.build_sales_invoices(qs_filtered)
        elif invoice_type == "purchase":
            data = InvoiceReportService.build_purchase_invoices(qs_filtered)
        else:
            data = list(
                qs_filtered.values(
                    "id", "number_invoice", "created_at", "state", "pdf_generated"
                )
            )

        summary = InvoiceReportService.get_summary(qs_filtered)

        return Response(
            {"summary": InvoiceSummarySerializer(summary).data, "data": data}
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(name="type", type=str, enum=["sale", "purchase"]),
        ]
    )
    @action(detail=False, methods=["get"], url_path="pdf")
    def invoices_pdf(self, request):
        invoice_type = request.query_params.get("type")
        company = CompanyService.get_active_company()
        qs = self.get_filtered_queryset(Invoice.objects.all(), InvoiceReportFilter)

        if invoice_type == "sale":
            qs = qs.filter(invoice_type=InvoiceType.SALE)
            invoices = InvoiceReportService.build_sales_invoices(qs)
            title = "Reporte de Facturas de Ventas"
            headers = ["Número", "Fecha", "Cliente", "Total", "Estado"]
            data_rows = [
                {
                    "values_list": [
                        inv["number_invoice"],
                        (
                            inv["created_at"].strftime("%d/%m/%Y")
                            if hasattr(inv["created_at"], "strftime")
                            else inv["created_at"]
                        ),
                        f"{inv.get('sale__customer__first_name', '')} {inv.get('sale__customer__last_name', '')}".strip()
                        or "Anónimo",
                        format_currency(inv["sale__total_amount"]),
                        {
                            "is_badge": True,
                            "text": (
                                "Emitida" if inv["state"] == "ISSUED" else "Cancelada"
                            ),
                            "badge_type": (
                                "success" if inv["state"] == "ISSUED" else "danger"
                            ),
                        },
                    ]
                }
                for inv in invoices
            ]
        elif invoice_type == "purchase":
            qs = qs.filter(invoice_type=InvoiceType.PURCHASE)
            invoices = InvoiceReportService.build_purchase_invoices(qs)
            title = "Reporte de Facturas de Compras"
            headers = ["Número", "Fecha", "Proveedor", "Total", "Estado"]
            data_rows = [
                {
                    "values_list": [
                        inv["number_invoice"],
                        (
                            inv["created_at"].strftime("%d/%m/%Y")
                            if hasattr(inv["created_at"], "strftime")
                            else inv["created_at"]
                        ),
                        inv.get("purchase__supplier__name", "N/A"),
                        format_currency(inv["purchase__total_amount"]),
                        {
                            "is_badge": True,
                            "text": (
                                "Emitida" if inv["state"] == "ISSUED" else "Cancelada"
                            ),
                            "badge_type": (
                                "success" if inv["state"] == "ISSUED" else "danger"
                            ),
                        },
                    ]
                }
                for inv in invoices
            ]
        else:
            invoices = list(
                qs.values(
                    "number_invoice",
                    "created_at",
                    "sale__customer__first_name",
                    "sale__customer__last_name",
                    "purchase__supplier__name",
                    "sale__total_amount",
                    "purchase__total_amount",
                    "state",
                )
            )
            title = "Reporte General de Facturas"
            headers = ["Número", "Fecha", "Cliente/Prov", "Total", "Estado"]
            data_rows = []
            for inv in invoices:
                name = (
                    f"{inv.get('sale__customer__first_name', '')} {inv.get('sale__customer__last_name', '')}".strip()
                    or inv.get("purchase__supplier__name")
                    or "N/A"
                )
                amount = inv.get("sale__total_amount") or inv.get(
                    "purchase__total_amount"
                )
                data_rows.append(
                    {
                        "values_list": [
                            inv["number_invoice"],
                            (
                                inv["created_at"].strftime("%d/%m/%Y")
                                if hasattr(inv["created_at"], "strftime")
                                else inv["created_at"]
                            ),
                            name,
                            format_currency(amount),
                            {
                                "is_badge": True,
                                "text": (
                                    "Emitida"
                                    if inv["state"] == "ISSUED"
                                    else "Cancelada"
                                ),
                                "badge_type": (
                                    "success" if inv["state"] == "ISSUED" else "danger"
                                ),
                            },
                        ]
                    }
                )

        summary = InvoiceReportService.get_summary(qs)
        kpis = [
            {"label": "Total Facturas", "value": summary["total_invoices"]},
            {
                "label": "Emitidas",
                "value": summary["issued_invoices"],
                "highlight": True,
            },
            {
                "label": "Canceladas",
                "value": summary["canceled_invoices"],
                "danger": True,
            },
            {"label": "PDFs", "value": summary["pdf_generated"]},
        ]

        context = {
            "title": title,
            "company": company,
            "kpis": kpis,
            "sections": [
                {"headers": headers, "data": data_rows, "align_last_right": True}
            ],
            "now": timezone.now(),
        }

        html_content = render_to_string("pdf/base_report.html", context)
        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reporte_facturas.pdf"'
        return response


class ReturnReportViewSet(ReportFilterMixin, viewsets.ViewSet):
    """
    Expone reportes relacionados con las devoluciones (ventas y compras).
    Utiliza el parámetro 'type' para alternar entre ventas y compras.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name="type", type=str, enum=["sale", "purchase"]),
        ],
        responses={200: ReturnReportSummarySerializer},
    )
    def list(self, request):
        return_type = request.query_params.get("type", "sale")

        if return_type == "purchase":
            qs = self.get_filtered_queryset(
                PurchaseReturn.objects.all(), PurchaseReturnReportFilter
            )
            summary = PurchaseReturnReportService.get_summary(qs)
            data = PurchaseReturnReportService.format_returns(qs)
            return Response(
                {
                    "summary": ReturnReportSummarySerializer(summary).data,
                    "data": ReturnDetailReportSerializer(data, many=True).data,
                }
            )

        # Default: Sale returns
        qs = self.get_filtered_queryset(
            SaleReturn.objects.all(), SaleReturnReportFilter
        )
        summary = SaleReturnReportService.get_summary(qs)
        data = SaleReturnReportService.format_returns(qs)
        return Response(
            {
                "summary": ReturnReportSummarySerializer(summary).data,
                "data": ReturnDetailReportSerializer(data, many=True).data,
            }
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(name="type", type=str, enum=["sale", "purchase"]),
        ]
    )
    @action(detail=False, methods=["get"], url_path="pdf")
    def returns_pdf(self, request):
        return_type = request.query_params.get("type", "sale")
        company = CompanyService.get_active_company()

        if return_type == "purchase":
            qs = self.get_filtered_queryset(
                PurchaseReturn.objects.select_related(
                    "purchase", "purchase__supplier"
                ).all(),
                PurchaseReturnReportFilter,
            )
            data = PurchaseReturnReportService.get_summary(qs)
            returns_data = PurchaseReturnReportService.format_returns(qs)
            title = "Reporte de Devoluciones (Compras)"
            headers = ["Fecha", "Proveedor", "Motivo", "Total Reembolso", "Estado"]
            data_rows = [
                {
                    "values_list": [
                        (
                            item["created_at"].strftime("%d/%m/%Y")
                            if hasattr(item["created_at"], "strftime")
                            else item["created_at"]
                        ),
                        item.get("supplier_name", "N/A"),
                        item["reason"],
                        format_currency(item["total_amount"]),
                        {
                            "is_badge": True,
                            "text": (
                                "Completada"
                                if item["state"] == "COMPLETED"
                                else "Pendiente"
                            ),
                            "badge_type": (
                                "success" if item["state"] == "COMPLETED" else "warning"
                            ),
                        },
                    ]
                }
                for item in returns_data
            ]
        else:
            qs = self.get_filtered_queryset(
                SaleReturn.objects.select_related("sale", "sale__customer").all(),
                SaleReturnReportFilter,
            )
            data = SaleReturnReportService.get_summary(qs)
            returns_data = SaleReturnReportService.format_returns(qs)
            title = "Reporte de Devoluciones (Ventas)"
            headers = ["Fecha", "Cliente", "Motivo", "Total Reembolso", "Estado"]
            data_rows = [
                {
                    "values_list": [
                        (
                            item["created_at"].strftime("%d/%m/%Y")
                            if hasattr(item["created_at"], "strftime")
                            else item["created_at"]
                        ),
                        item.get("customer_name", "Anónimo"),
                        item["reason"],
                        format_currency(item["total_amount"]),
                        {
                            "is_badge": True,
                            "text": (
                                "Completada"
                                if item["state"] == "COMPLETED"
                                else "Pendiente"
                            ),
                            "badge_type": (
                                "success" if item["state"] == "COMPLETED" else "warning"
                            ),
                        },
                    ]
                }
                for item in returns_data
            ]

        kpis = [
            {"label": "Total Devoluciones", "value": data["total_returns"]},
            {
                "label": "Monto Total",
                "value": format_currency(data["total_refund_amount"]),
                "highlight": True,
            },
        ]

        context = {
            "title": title,
            "company": company,
            "kpis": kpis,
            "sections": [
                {"headers": headers, "data": data_rows, "align_last_right": True}
            ],
            "now": timezone.now(),
        }

        html_content = render_to_string("pdf/base_report.html", context)
        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reporte_devoluciones.pdf"'
        return response
