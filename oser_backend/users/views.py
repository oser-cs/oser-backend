"""Users API views."""

from django.contrib.auth import get_user_model
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from tutoring.serializers import TutoringGroupSerializer
from visits.serializers import VisitSerializer

from .models import Student, Tutor
from .serializers import StudentSerializer, TutorSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows users to be viewed or edited.

    retrieve:
    Return a user instance.

    list:
    Return all users.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (DRYPermissions,)


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
    """API endpoint that allows students to be viewed."""

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
