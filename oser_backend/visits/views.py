"""Visits API views."""

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.decorators import list_route
from dry_rest_permissions.generics import DRYPermissions
from .serializers import VisitSerializer, PlaceSerializer
from .serializers import VisitParticipantReadSerializer
from .serializers import VisitParticipantWriteSerializer
from .serializers import VisitParticipantIdentifySerializer
from .serializers import VisitParticipantDetailSerializer
from .models import Visit, VisitParticipant, Place
from users.models import User


class VisitViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoints that allows visits to be viewed."""

    serializer_class = VisitSerializer
    queryset = Visit.objects.all()
    permission_classes = (DRYPermissions,)


class VisitParticipantsViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """API endpoints to manage participants of visits."""

    permission_classes = (DRYPermissions,)

    def get_queryset(self):
        """Determine, among other things, what get_object() will return.

        Return all visits for the retrieve action as the <pk> identifies
        a visit there.
        Otherwise return all visit participants.
        """
        if self.action == 'retrieve':
            return Visit.objects.all()
        return VisitParticipant.objects.all()

    def get_serializer_class(self):
        """Return the right serializer class for each action.

        Allows DRF to display arguments/parameters in the generated docs.
        """
        if self.action == 'list':
            return VisitParticipantReadSerializer
        elif self.action == 'retrieve':
            return VisitParticipantDetailSerializer
        elif self.action == 'get_id':
            return VisitParticipantIdentifySerializer
        else:
            return VisitParticipantWriteSerializer

    def retrieve(self, request, pk=None):
        """Retrieve the participants to a visit."""
        visit = self.get_object()
        participants = VisitParticipant.objects.filter(visit=visit)
        serializer = self.get_serializer(participants, many=True,
                                         context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['put'], url_path='get-id')
    def get_id(self, request):
        """Special endpoint to get ID of participant from user and visit.

        Useful to perform a DELETE request afterwards (which only accepts
        a participant ID).
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, pk=serializer.validated_data['user_id'])
            visit = get_object_or_404(
                Visit, pk=serializer.validated_data['visit_id'])
            participant = get_object_or_404(VisitParticipant,
                                            user=user,
                                            visit=visit)
            return Response({'id': participant.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    """Simple read-only view set for places."""

    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
