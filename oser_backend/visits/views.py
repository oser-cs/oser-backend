from rest_framework import viewsets
from dry_rest_permissions.generics import DRYPermissions
from .serializers import VisitSerializer
from .models import Visit


class VisitViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows visits to be viewed."""

    serializer_class = VisitSerializer
    queryset = Visit.objects.all()
    permission_classes = (DRYPermissions,)
