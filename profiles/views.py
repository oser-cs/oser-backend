"""Profile API views."""

from django.contrib.auth import get_user_model
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from tutoring.serializers import TutoringGroupSerializer
from visits.serializers import VisitSerializer

from .models import Student, Tutor
from .serializers import StudentSerializer, TutorSerializer


User = get_user_model()


class TutorViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows tutors to be viewed."""

    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    permission_classes = (DRYPermissions,)

    @action(detail=True)
    def tutoringgroups(self, request, pk=None):
        """Retrieve the tutoring groups of a tutor."""
        tutor = self.get_object()
        tutoring_groups = tutor.tutoring_groups.all()
        serializer = TutoringGroupSerializer(tutoring_groups, many=True,
                                             context={'request': request})
        return Response(serializer.data)


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
                "gender": null,
                "phone_number": null,
                "date_of_birth": null,
                "url": "http://localhost:8000/api/users/4/"
            },
            "address": {
                "line1": "88 bis rue Jules Guesde",
                "line2": "",
                "post_code": "93100",
                "city": "Montreuil",
                "country": {
                    "code": "FR",
                    "name": "France"
                }
            },
            "tutoring_group": 1,
            "school": "0930965U",
            "emergency_contact": {
                "first_name": "Marie-Claude",
                "last_name": "Perret",
                "email": null,
                "home_phone": "+33312344556",
                "mobile_phone": null
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
    def tutoringgroup(self, request, pk=None):
        """Retrieve the tutoring group of a student."""
        student = self.get_object()
        tutoring_group = student.tutoring_group
        serializer = TutoringGroupSerializer(tutoring_group,
                                             context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def visits(self, request, pk=None):
        """List detailed info about the visits a student participates in."""
        # NOTE: Only available for student users for now.
        user = User.objects.get(pk=pk)
        visits = user.visit_set.all()
        serializer = VisitSerializer(visits, many=True,
                                     context={'request': request})
        return Response(serializer.data)
