"""Users API views."""

from rest_framework import viewsets
from users.models import User
from api.serializers.users import UserSerializer

# Create your views here.


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """List and detail views for users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
