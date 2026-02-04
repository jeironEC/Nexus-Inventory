# Django
from django.urls import path

# Rest framework
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

# Views
from .views import EmailTokenObtainPairViewSet

urlpatterns = [
    path("token/", EmailTokenObtainPairViewSet.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
