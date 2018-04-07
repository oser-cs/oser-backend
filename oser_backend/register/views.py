"""Register views."""

from dry_rest_permissions.generics import DRYPermissions
from rest_framework import mixins, viewsets

from .models import Registration
from .serializers import RegistrationSerializer


# Create your views here.


class RegistrationViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """API endpoints to create and list registrations."""

    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (DRYPermissions,)
