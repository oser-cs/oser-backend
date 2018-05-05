"""Users API views."""

from django.contrib.auth import get_user_model
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import viewsets
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows users to be viewed.

    retrieve:
    Return a user instance.

    list:
    Return all users.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (DRYPermissions,)
