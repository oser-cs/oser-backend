"""Projects views."""

from rest_framework import mixins, permissions, viewsets

from django_filters import rest_framework as filters

from .models import Edition, Participation, Project
from .serializers import (EditionDetailSerializer, EditionListSerializer,
                          ParticipationSerializer, ProjectDetailSerializer,
                          ProjectSerializer)


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
            "description": "Oser la Prépa est un stage d'acclimatation…",
            "logo": null,
            "editions": [
                {
                    "id": 1,
                    "url": "http://localhost:8000/api/editions/1/",
                    "name": "",
                    "year": 2018,
                    "project": 1,
                    "description": "",
                    "organizers": 0,
                    "participations": 2,
                    "edition_form": {
                        "id": 1,
                        "edition": 1,
                        "deadline": "2018-06-30"
                    }
                }
            ]
        }

    """

    queryset = Project.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectSerializer


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
                "project": 1,
                "description": "",
                "organizers": 0,
                "participations": 2,
                "edition_form": {
                    "id": 1,
                    "edition": 1,
                    "deadline": "2018-06-30"
                }
            }
        ]

    retrieve:

    Retrieve a specific edition.

    Each `participation` in `participations` has the following format:

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

    ### Example response

        {
            "id": 1,
            "url": "http://localhost:8000/api/editions/1/",
            "name": "",
            "year": 2018,
            "project": 1,
            "description": "",
            "organizers": [],
            "participations": [],
            "edition_form": {
                "id": 1,
                "edition": 1,
                "deadline": "2018-06-30",
                "form": {
                    "id": 2,
                    "url": "http://localhost:8000/api/forms/2/",
                    "slug": "inscriptions-a-oser-la-prepa-2018",
                    "title": "Inscription à Oser la Prépa 2018",
                    "entries_count": 1,
                    "sections": [
                        {
                            "id": 1,
                            "title": "Enfant",
                            "form": 2,
                            "questions": [
                                {
                                    "id": 14,
                                    "type": "text-small",
                                    "text": "Nom",
                                    "help_text": "",
                                    "required": true,
                                    "section": 1
                                },
                            ]
                        }
                    ],
                    "files": [
                        {
                            "id": 1,
                            "name": "Autorisation parentale",
                            "file": "http://localhost:8000/file.pdf",
                            "form": 2
                        }
                    ]
                },
                "recipient": {
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
                    "address": {
                        "line1": "Rue de Rivoli",
                        "line2": "",
                        "post_code": "75001",
                        "city": "Paris",
                        "country": {
                            "code": "FR",
                            "name": "France"
                        }
                    },
                    "promotion": 2020,
                    "tutoring_groups": [
                        1
                    ],
                    "url": "http://localhost:8000/api/tutors/1/"
                }
            }
        }
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
