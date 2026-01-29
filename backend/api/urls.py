from django.urls import path
from .views import healthcheck

urlpatterns = [
    path("health/", healthcheck, name="health"),  # Endpoint verifica estado del sistema
]
