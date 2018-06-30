"""Projects views."""

from django.shortcuts import redirect
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from django_filters import rest_framework as filters
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from dynamicforms.serializers import FormEntrySerializer

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
                "project": "Oser la Prépa",
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

    queryset = Edition.objects.all().prefetch_related(
        'participations', 'organizers'
    )
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('project', 'year',)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EditionDetailSerializer
        return EditionListSerializer

    @action(methods=['get'], detail=False)
    def open_registrations(self, request, **kwargs):
        """Return a list of the editions with open registrations.

        These are the editions that have an edition form set and whose
        deadline is a future date.

        ### Example response

            [
                {
                    "id": 1,
                    "url": "http://localhost:8000/api/editions/1/",
                    "name": "",
                    "year": 2018,
                    "project": "Oser la Prépa",
                    "description": "",
                    "organizers": 0,
                    "participations": 3,
                    "edition_form": {
                        "id": 1,
                        "edition": 1,
                        "deadline": "2018-06-30"
                    }
                }
            ]
        """
        queryset = self.get_queryset().filter(
            edition_form__isnull=False,
            edition_form__deadline__gte=now().date())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def form(self, request, pk=None):
        """Return the edition's form.

        If the edition does not have a form,
        returns a `404 Not Found` error response.

        ### Example response

        See [forms: read](#forms-read).
        """
        edition = self.get_object()
        try:
            form = edition.edition_form.form
        except ObjectDoesNotExist:
            return Response(
                {'detail': 'No form set on this edition.'}, status=404)
        else:
            return redirect('api:form-detail', str(form.pk))


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
                "edition_id": 1,
                "edition_form_title": "Inscriptions à Oser la Prépa 2018"
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
            "edition_id": 1,
            "edition_form_title": "Inscriptions à Oser la Prépa 2018"
            "state": "valid"
        }
    """

    queryset = Participation.objects.prefetch_related('edition').all()
    serializer_class = ParticipationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'state',)

    @action(methods=['get'], detail=True)
    def form_entry(self, request, pk=None):
        """Return the answers to the edition form for a participation.

        ### Example response

            {
                "id": 20,
                "form": 4,
                "submitted": "2018-06-30T09:43:28.779628+02:00",
                "answers": [
                    {
                        "id": 79,
                        "question": 40,
                        "entry": 20,
                        "answer": "Florimond"
                    }
                ]
            }
        """
        participation = self.get_object()
        serializer = FormEntrySerializer(participation.entry)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
