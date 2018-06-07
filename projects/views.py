"""Projects views."""

from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets, permissions

from .models import Edition, Participation, Project
from .serializers import (EditionDetailSerializer, EditionListSerializer,
                          ParticipationSerializer, ProjectSerializer)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve projects.

    list:

    Get a list of the projects.

    ### Example response

        [
            {
                "id": 2,
                "url": "http://localhost:8000/api/projects/2/",
                "name": "(Art)cessible",
                "description": "",
                "logo": null
            },
            {
                "id": 1,
                "url": "http://localhost:8000/api/projects/1/",
                "name": "Oser la Prépa",
                "description": "Oser la Prépa est un stage d'acclimatation aux Classes Préparatoires de deux semaines qui se déroule chaque été.",
                "logo": null
            }
        ]

    retrieve:

    Retrieve a specific project.

    ### Example response

        {
            "id": 1,
            "url": "http://localhost:8000/api/projects/1/",
            "name": "Oser la Prépa",
            "description": "Oser la Prépa est un stage d'acclimatation aux Classes Préparatoires de deux semaines qui se déroule chaque été.",
            "logo": null
        }

    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)


class EditionViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve project editions.

    list:

    Get a list of project editions.

    You can filter the list using query parameters:

    - `project`: the ID of a project. Only editions for that project will be
    returned.
    - `year`: an integer. Only editions for that year will be returned.

    ### Example response

        [
            {
                "id": 1,
                "url": "http://localhost:8000/api/editions/1/",
                "name": "",
                "year": 2018,
                "project": {
                    "id": 1,
                    "url": "http://localhost:8000/api/projects/1/",
                    "name": "Oser la Prépa",
                    "description": "Oser la Prépa est un stage…",
                    "logo": null
                },
                "description": "",
                "organizers": 0,
                "participations": 1
            }
        ]

    retrieve:

    Retrieve a specific edition.

    ### Example response

        [
            {
                "id": 1,
                "url": "http://localhost:8000/api/editions/1/",
                "name": "",
                "year": 2018,
                "project": {
                    "id": 1,
                    "url": "http://localhost:8000/api/projects/1/",
                    "name": "Oser la Prépa",
                    "description": "Oser la Prépa est un stage…",
                    "logo": null
                },
                "description": "",
                "organizers": [ ],
                "participations": [
                {
                    "id": 3,
                    "submitted": "2018-06-07T00:31:37.947085+02:00",
                    "user": {
                    "id": 3,
                    "email": "john.doe@example.com",
                    "profile_type": null,
                    "first_name": "John",
                    "last_name": "Doe",
                    "gender": null,
                    "phone_number": "+33 6 12 34 56 78",
                    "date_of_birth": null,
                    "url": "http://localhost:8000/api/users/3/"
                },
                "edition": 1,
                "state": "valid"
            },
        ]
    """

    queryset = Edition.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('project', 'year',)

    def get_serializer_class(self):
        if self.action == 'list':
            return EditionListSerializer
        elif self.action == 'retrieve':
            return EditionDetailSerializer


class ParticipationViewSet(mixins.CreateModelMixin,
                           viewsets.ReadOnlyModelViewSet):
    """Endpoints for manipulating participations to project editions.

    list:

    Get a list of participations.

    ### Example response

        [
            {
                "id": 3,
                "submitted": "2018-06-07T00:31:37.947085+02:00",
                "user": {
                    "id": 3,
                    "email": "john.doe@example.com",
                    "profile_type": null,
                    "first_name": "John",
                    "last_name": "Doe",
                    "gender": null,
                    "phone_number": "+33 6 12 34 56 78",
                    "date_of_birth": null,
                    "url": "http://localhost:8000/api/users/3/"
                },
                "edition": 1,
                "state": "valid"
            },
        ]

    retrieve:

    Retrieve a specific participation.

    ### Example response

        {
            "id": 3,
            "submitted": "2018-06-07T00:31:37.947085+02:00",
            "user": {
                "id": 3,
                "email": "john.doe@example.com",
                "profile_type": null,
                "first_name": "John",
                "last_name": "Doe",
                "gender": null,
                "phone_number": "+33 6 12 34 56 78",
                "date_of_birth": null,
                "url": "http://localhost:8000/api/users/3/"
            },
            "edition": 1,
            "state": "valid"
        }
    """

    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer
    permission_classes = (permissions.IsAuthenticated,)
