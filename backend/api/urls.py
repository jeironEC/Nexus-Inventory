# Django
from django.urls import path, include

# Rest framework
from rest_framework.routers import SimpleRouter

# Views
from .views import healthcheck, UserViewSet, UserMeViewSet

router = SimpleRouter(use_regex_path=False)

router.register("users", UserViewSet, basename="users")
router.register("users", UserMeViewSet, basename="user")

urlpatterns = [
    path("health/", healthcheck, name="health"),  # Endpoint verifica estado del sistema
    path("", include("api.docs")),
    *router.urls,
]
