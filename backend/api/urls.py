# Django
from django.urls import path, include

# Rest framework
from rest_framework.routers import SimpleRouter

# DRF Nested Routers
from rest_framework_nested import routers

# Views
from .views import (
    HealthCheckView,
    UserRoleViewSet,
    UserViewSet,
    UserMeViewSet,
    PasswordResetViewSet,
    CompanyViewSet,
    CategoryViewSet,
    ProductViewSet,
    InventoryViewSet,
    InventoryMovementViewSet,
    CustomerViewSet,
    SaleViewSet,
    SaleDetailViewSet,
    SaleReturnViewSet,
    SaleReturnDetailViewSet,
    InvoiceViewSet,
    SupplierViewSet,
    PurchaseViewSet,
    PurchaseDetailViewSet,
    PurchaseReturnViewSet,
    PurchaseReturnDetailViewSet,
    SaleReportViewSet,
    PurchaseReportViewSet,
    InventoryReportViewSet,
    ProductReportViewSet,
    CustomerReportViewSet,
    InvoiceReportViewSet,
    SaleReturnReportViewSet,
    PurchaseReturnReportViewSet,
)

router = SimpleRouter()

router.register("users", UserViewSet, basename="users")
router.register("users", UserMeViewSet, basename="user")
router.register(r"password-reset", PasswordResetViewSet, basename="password-reset")
router.register("roles", UserRoleViewSet, basename="roles")
router.register("companies", CompanyViewSet, basename="companies")
router.register("categories", CategoryViewSet, basename="categories")
router.register("products", ProductViewSet, basename="products")
router.register("inventories", InventoryViewSet, basename="inventories")
router.register(
    "inventory-movements", InventoryMovementViewSet, basename="inventory-movements"
)
router.register("customers", CustomerViewSet, basename="customers")
router.register("sales", SaleViewSet, basename="sales")
sale_router = routers.NestedSimpleRouter(router, "sales", lookup="sales")
sale_router.register("details", SaleDetailViewSet, basename="sale-detail")
router.register("sale-returns", SaleReturnViewSet, basename="sale-returns")
sale_return_router = routers.NestedSimpleRouter(
    router, "sale-returns", lookup="sale_returns"
)
sale_return_router.register(
    "details", SaleReturnDetailViewSet, basename="sale-return-detail"
)
router.register("invoices", InvoiceViewSet, basename="invoices")
router.register("suppliers", SupplierViewSet, basename="suppliers")
router.register("purchases", PurchaseViewSet, basename="purchases")
purchase_router = routers.NestedSimpleRouter(router, "purchases", lookup="purchases")
purchase_router.register("details", PurchaseDetailViewSet, basename="purchase-detail")
router.register("purchase-returns", PurchaseReturnViewSet, basename="purchase-returns")
purchase_return_router = routers.NestedSimpleRouter(
    router, "purchase-returns", lookup="purchase_returns"
)
purchase_return_router.register(
    "details", PurchaseReturnDetailViewSet, basename="purchase-return-detail"
)
router.register("reports", SaleReportViewSet, basename="sale-reports")
router.register("reports", PurchaseReportViewSet, basename="purchase-reports")
router.register("reports", InventoryReportViewSet, basename="inventory-reports")
router.register("reports", ProductReportViewSet, basename="product-reports")
router.register("reports", CustomerReportViewSet, basename="customer-reports")
router.register("reports", InvoiceReportViewSet, basename="invoice-reports")
router.register("reports", SaleReturnReportViewSet, basename="sale-return-reports")
router.register(
    "reports", PurchaseReturnReportViewSet, basename="purchase-return-reports"
)

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("", include("api.docs")),
    path("auth/", include("api.auth")),
    *router.urls,
    *sale_router.urls,
    *sale_return_router.urls,
    *purchase_router.urls,
    *purchase_return_router.urls,
]
