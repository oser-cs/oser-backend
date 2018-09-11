"""Profile API views."""

from django.contrib.auth import get_user_model
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from visits.serializers import VisitSerializer

from .models import Student, Tutor
from .serializers import StudentSerializer, TutorSerializer


User = get_user_model()


class TutorViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows tutors to be viewed."""

    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    permission_classes = (DRYPermissions,)


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows students to be viewed.

    list:

    ### Example response

    List of results from `retrieve` (see the example response for `retrieve`).

    retrieve:

    ### Example response

        {
            "user_id": 4,
            "user": {
                "id": 4,
                "email": "charles.dumont@example.net",
                "profile_type": null,
                "first_name": "",
                "last_name": "",
                "url": "http://localhost:8000/api/users/4/"
            },
            "registration": {
                "id": 3,
                "submitted": "2018-05-05T14:15:10.998206+02:00",
                "validated": false
            },
            "visits": [],
            "url": "http://localhost:8000/api/students/2/"
        }
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (DRYPermissions,)

    @action(detail=True)
    def visits(self, request, pk=None):
        """List detailed info about the visits a student participates in."""
        # NOTE: Only available for student users for now.
        user = User.objects.get(pk=pk)
        visits = user.visit_set.all()
        serializer = VisitSerializer(visits, many=True,
                                     context={'request': request})
        return Response(serializer.data)
