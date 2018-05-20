"""Visits API views."""

from django.shortcuts import get_object_or_404
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from users.models import User

from .models import Participation, Place, Visit
from .serializers import (ParticipationIdentifySerializer,
                          ParticipationWriteSerializer, PlaceSerializer,
                          VisitListSerializer, VisitSerializer)


class VisitViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoints that allows visits to be viewed.

    When the current user participates in a visit, a `"participates": true`
    field is present.

    list:

    List visits and retrieve partial information about them.

    ### Example response

        [
            {
                "id": 1,
                "title": "Visite du Palais de la Découverte",
                "summary": "",
                "place": "Palais de la Découverte",
                "date": "2018-05-30T14:00:00+02:00",
                "deadline": "2018-05-28T23:59:00+02:00",
                "passed": false,
                "registrations_open": true,
                "participants": [4],
                "organizers": [3],
                "image": "http://localhost:8000/media/visits/images/visit-1.jpg",
                "url": "http://localhost:8000/api/visits/1/"
            }
        ]

    retrieve:

    Retrieve details about a visit.

    ### Example response

        {
            "id": 1,
            "title": "Visite du Palais de la Découverte",
            "summary": "",
            "description": "",
            "place": {
                "id": 1,
                "name": "Palais de la Découverte",
                "address": {
                    "line1": "Avenue Franklin Delano Roosevelt",
                    "line2": "",
                    "post_code": "75008",
                    "city": "Paris",
                    "country": {
                        "code": "FR",
                        "name": "France"
                    }
                },
                "description": ""
            },
            "date": "2018-05-30T14:00:00+02:00",
            "passed": false,
            "deadline": "2018-05-28T23:59:00+02:00",
            "registrations_open": true,
            "participants": [
                {
                    "id": 1,
                    "user": {
                        "id": 4,
                        "email": "charles.dumont@example.net",
                        "profile_type": null,
                        "first_name": "",
                        "last_name": "",
                        "gender": null,
                        "phone_number": null,
                        "date_of_birth": null,
                        "url": "http://localhost:8000/api/users/4/"
                    },
                    "present": null,
                    "accepted": null
                }
            ],
            "organizers": [
                {
                    "id": 1,
                    "user": {
                        "id": 3,
                        "email": "john.doe@example.com",
                        "profile_type": null,
                        "first_name": "John",
                        "last_name": "Doe",
                        "gender": null,
                        "phone_number": null,
                        "date_of_birth": null,
                        "url": "http://localhost:8000/api/users/3/"
                    }
                }
            ],
            "attached_files": [
                {
                    "id": 1,
                    "name": "Autorisation de sortie",
                    "required": true
                }
            ],
            "image": "http://localhost:8000/media/visits/images/visit1.jpg",
            "fact_sheet": "http://localhost:8000/media/visits/fact_sheets/visit1-factsheet.pdf",
            "url": "http://localhost:8000/api/visits/1/"
        }

    """

    serializer_class = VisitSerializer
    queryset = Visit.objects.all()
    permission_classes = [DRYPermissions]

    def get_serializer_class(self):
        if self.action == 'list':
            return VisitListSerializer
        else:
            return VisitSerializer


class ParticipationsViewSet(mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """API endpoints to manage participants of visits."""

    permission_classes = [DRYPermissions]
    queryset = Participation.objects.all()

    def get_serializer_class(self):
        """Return the right serializer class for each action."""
        if self.action == 'get_id':
            return ParticipationIdentifySerializer
        else:
            return ParticipationWriteSerializer

    @list_route(methods=['put'], url_path='get-id')
    def get_id(self, request):
        """Get ID of participant from user and visit.

        Useful to perform a DELETE request afterwards (which only accepts
        a participant ID).
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, pk=serializer.validated_data['user_id'])
            visit = get_object_or_404(
                Visit, pk=serializer.validated_data['visit_id'])
            participant = get_object_or_404(Participation,
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
