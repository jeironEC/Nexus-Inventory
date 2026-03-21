# Django
from django.urls import path, include

# Rest framework
from rest_framework.routers import SimpleRouter

# DRF Nested Routers
from rest_framework_nested import routers

# Views
from .views import (
    healthcheck,
    UserRoleViewSet,
    UserViewSet,
    UserMeViewSet,
    CategoryViewSet,
    ProductViewSet,
    InventoryViewSet,
    InventoryMovementViewSet,
    CustomerViewSet,
    PromotionViewSet,
    CustomerPromotionViewSet,
    SaleViewSet,
    SaleDetailViewSet,
    InvoiceViewSet,
    SupplierViewSet,
    PurchaseViewSet,
)

router = SimpleRouter()

router.register("users", UserViewSet, basename="users")
router.register("users", UserMeViewSet, basename="user")
router.register("roles", UserRoleViewSet, basename="roles")
router.register("categories", CategoryViewSet, basename="categories")
router.register("products", ProductViewSet, basename="products")
router.register("inventories", InventoryViewSet, basename="inventories")
router.register(
    "inventory_movements", InventoryMovementViewSet, basename="inventory_movements"
)
router.register("customers", CustomerViewSet, basename="customers")
router.register("promotions", PromotionViewSet, basename="promotions")
router.register(
    "customer_promotions", CustomerPromotionViewSet, basename="customer_promotions"
)
router.register("sales", SaleViewSet, basename="sales")


sale_router = routers.NestedSimpleRouter(router, "sales", lookup="sales")
sale_router.register("details", SaleDetailViewSet, basename="sale-detail")
router.register("invoices", InvoiceViewSet, basename="invoices")
router.register("suppliers", SupplierViewSet, basename="suppliers")
router.register("purchases", PurchaseViewSet, basename="purchases")

urlpatterns = [
    path("health/", healthcheck, name="health"),
    path("", include("api.docs")),
    path("auth/", include("api.auth")),
    *router.urls,
    *sale_router.urls,
]
