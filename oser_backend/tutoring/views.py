"""Tutoring API views."""

from rest_framework.viewsets import ReadOnlyModelViewSet
from dry_rest_permissions.generics import DRYPermissions

from .models import TutoringGroup, School, TutoringSession
from .serializers import (
    TutoringGroupSerializer,
    SchoolSerializer,
    TutoringSessionSerializer,
)

# Create your views here.


class TutoringGroupViewSet(ReadOnlyModelViewSet):
    """API endpoint that allows tutoring groups to be viewed or edited.

    Actions: list, retrieve, create, update, partial_update, destroy
    """

    queryset = TutoringGroup.objects.all()
    serializer_class = TutoringGroupSerializer
    permission_classes = (DRYPermissions,)

    def get_queryset(self):
        queryset = self.queryset
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class SchoolViewSet(ReadOnlyModelViewSet):
    """API endpoint that allows schools to be viewed.

    list:

    List all schools.

    ### Example response

        [
            {
                "uai_code": "0930965U",
                "url": "http://localhost:8000/api/schools/0930965U/",
                "name": "Henri Matisse",
                "address": {
                    "line1": "88 Bis rue Rules Guesde",
                    "line2": "",
                    "post_code": "93100",
                    "city": "Montreuil",
                    "country": {
                        "code": "FR",
                        "name": "France"
                    }
                },
                "students": [ ],
                "students_count": 0
            }
        ]

    retrieve:

    Retrieve information about a specific school.

    ### Example response

        {
            "uai_code": "0930965U",
            "url": "http://localhost:8000/api/schools/0930965U/",
            "name": "Henri Matisse",
            "address": {
                "line1": "88 Bis rue Rules Guesde",
                "line2": "",
                "post_code": "93100",
                "city": "Montreuil",
                "country": {
                "code": "FR",
                "name": "France"
                }
            },
            "students": [ ],
            "students_count": 0
        }
    """

    queryset = School.objects.all()
    permission_classes = (DRYPermissions,)

    def get_queryset(self):
        queryset = self.queryset
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def get_serializer_class(self):
        return SchoolSerializer


class TutoringSessionViewSet(ReadOnlyModelViewSet):
    """API endpoint that allows tutoring sessions to be viewed or edited.

    Actions: list, retrieve, create, update, partial_update, destroy
    """

    queryset = TutoringSession.objects.all()
    serializer_class = TutoringSessionSerializer
