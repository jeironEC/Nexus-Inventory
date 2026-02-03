from django.urls import path, include
from .views import healthcheck

urlpatterns = [
    path("health/", healthcheck, name="health"),  # Endpoint verifica estado del sistema
    path("", include("api.docs")),
]
