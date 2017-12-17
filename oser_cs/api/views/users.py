"""Users API views."""

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin,
)
from users.models import Tutor, Student, SchoolStaffMember
from api.serializers.users import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    TutorSerializer, StudentSerializer, SchoolStaffMembersSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited.

    retrieve:
    Return a user instance.

    list:
    Return all users.

    create:
    Create a user instance.
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ('update', 'partial_update'):
            return UserUpdateSerializer
        return UserSerializer


class TutorViewSet(viewsets.ModelViewSet):
    """API endpoint that allows tutors to be viewed or edited.

    retrieve:
    Return a tutor instance.

    list:
    Return all tutors.

    create:
    Create a tutor instance.
    """

    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer


class StudentViewSet(ListModelMixin,
                     RetrieveModelMixin,
                     CreateModelMixin,
                     viewsets.GenericViewSet):
    """API endpoint that allows students to be viewed or edited.

    retrieve:
    Return a student instance.

    list:
    Return all students.

    create:
    Create a student instance.
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class SchoolStaffMemberViewSet(ListModelMixin,
                               RetrieveModelMixin,
                               CreateModelMixin,
                               viewsets.GenericViewSet):
    """API endpoint that allows school staff members to be viewed or edited.

    retrieve:
    Return a school staff member instance.

    list:
    Return all school staff members.

    create:
    Create a school staff member instance.
    """

    queryset = SchoolStaffMember.objects.all()
    serializer_class = SchoolStaffMembersSerializer
