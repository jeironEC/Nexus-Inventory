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
)

router = SimpleRouter(use_regex_path=False)

router.register("users", UserViewSet, basename="users")
router.register("users", UserMeViewSet, basename="user")
router.register("roles", UserRoleViewSet, basename="roles")
router.register("categories", CategoryViewSet, basename="categories")
router.register("products", ProductViewSet, basename="products")

urlpatterns = [
    path("health/", healthcheck, name="health"),  # Endpoint verifica estado del sistema
    path("", include("api.docs")),
    path("auth/", include("api.auth")),
    *router.urls,
]
