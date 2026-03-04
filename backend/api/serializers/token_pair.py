# Rest framework
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer para usar el email en lugar de username
    """

    username_field = "email"
