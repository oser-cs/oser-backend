"""Visits API views."""

from dry_rest_permissions.generics import DRYPermissions
from rest_framework import mixins, viewsets

from .models import Participation, Place, Visit
from .serializers import (ParticipationSerializer, PlaceSerializer,
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
            "date": "2018-05-30",
            "start_time": "14:00:00",
            "end_time": "16:00:00",
            "meeting": "Devant les escaliers de l'entrée principale",
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
                    "visit": 1,
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
            "image": "http://localhost:8000/media/visits/images/visit1.jpg",
            "fact_sheet": "http://localhost:8000/media/visits/fact_sheets/visit1.pdf",
            "permission": "http://localhost:8000/media/visits/visit_permissions/visit1.pdf",
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
    """API endpoints to manage visit participations.

    create:

    Add a participant to a visit.

    ### Example payload

        {
            "user": 3,
            "visit": 1
        }

    ### Example response

        {
            "id": 5,
            "visit": 1,
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
            },
            "present": null,
            "accepted": null
        }

    destroy:

    Remove a participant from a visit. No response data returned.

    """

    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer
    permission_classes = [DRYPermissions]


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    """Simple read-only view set for places."""

    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
