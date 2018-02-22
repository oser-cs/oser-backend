"""Visits API views."""

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from dry_rest_permissions.generics import DRYPermissions
from .serializers import VisitSerializer
from .serializers import VisitParticipantReadSerializer
from .serializers import VisitParticipantWriteSerializer
from .serializers import VisitParticipantDetailSerializer
from .models import Visit, VisitParticipant


class VisitViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoints that allows visits to be viewed."""

    serializer_class = VisitSerializer
    queryset = Visit.objects.all()
    permission_classes = (DRYPermissions,)

    @detail_route()
    def participants(self, request, pk=None):
        """List participants of a visit with their contact information."""
        visit = self.get_object()
        participants = VisitParticipant.objects.filter(visit=visit)
        serializer = VisitParticipantDetailSerializer(participants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VisitParticipantViewSet(viewsets.ModelViewSet):
    """API endpoints to manage participants of visits."""

    queryset = VisitParticipant.objects.all()
    permission_classes = (DRYPermissions,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return VisitParticipantReadSerializer
        else:
            return VisitParticipantWriteSerializer
