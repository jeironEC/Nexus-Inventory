# Django
from django.urls import path, include

# Rest framework
from rest_framework.routers import SimpleRouter

# Views
from .views import (
    healthcheck,
    UserRoleViewSet,
    UserViewSet,
    UserMeViewSet,
    CategoryViewSet,
    ProductViewSet,
    InventoryViewSet,
)

router = SimpleRouter(use_regex_path=False)

router.register("users", UserViewSet, basename="users")
router.register("users", UserMeViewSet, basename="user")
router.register("roles", UserRoleViewSet, basename="roles")
router.register("categories", CategoryViewSet, basename="categories")
router.register("products", ProductViewSet, basename="products")
router.register("inventories", InventoryViewSet, basename="inventories")

urlpatterns = [
    path("health/", healthcheck, name="health"),  # Endpoint verifica estado del sistema
    path("", include("api.docs")),  # Endpoints de documentación
    path("auth/", include("api.auth")),  # Endpoints de autenticación
    *router.urls,  # Endpoints de la API
]
