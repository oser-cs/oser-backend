"""Users API views."""

from django.contrib.auth import get_user_model
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from tutoring.serializers import TutoringGroupSerializer

from .models import SchoolStaffMember, Student, Tutor
from .serializers import (SchoolStaffMembersSerializer, StudentSerializer,
                          TutorSerializer, UserCreateSerializer,
                          UserSerializer, UserUpdateSerializer)

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
    permission_classes = (DRYPermissions,)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ('update', 'partial_update'):
            return UserUpdateSerializer
        return UserSerializer


class ProfileViewSetMeta(type):
    """Metaclass for ProfileViewSet.

    Automatically adds action to the concrete viewset docstring.
    """

    ACTIONS_DOCSTRING_TEMPLATE = """
    list:
    Return all {plural}.

    retrieve:
    Return a {singular} instance.

    create:
    Create a {singular} instance.

    destroy:
    Destroy a {singular} instance.

    update:
    Update a {singular} instance (requires full data about the instance).

    partial_update:
    Partially update a {singular} instance (e.g. a single attribute).
    """

    def __new__(metacls, name, bases, namespace):
        add_actions_docs = namespace.pop('add_actions_docs', True)
        cls = super().__new__(metacls, name, bases, namespace)
        if add_actions_docs:
            if not cls.__doc__:
                cls.__doc__ = ""
            if not hasattr(cls, 'queryset'):
                raise AttributeError('ProfileViewSet subclass must define '
                                     'a queryset attribute')
            # build the actions dosctring
            actions_doc = type(cls).ACTIONS_DOCSTRING_TEMPLATE.format(
                singular=cls.queryset.model._meta.model_name,
                plural=cls.queryset.model._meta.model_name + 's',
            )
            # append actions docstring to viewset's docstring.
            cls.__doc__ += actions_doc
        return cls


class ProfileViewSet(viewsets.ModelViewSet, metaclass=ProfileViewSetMeta):
    """Abstract viewset for profiles."""

    permission_classes = (DRYPermissions,)  # defined for all profile types
    add_actions_docs = False


class TutorViewSet(ProfileViewSet):
    """API endpoint that allows tutors to be viewed or edited."""

    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

    @detail_route()
    def tutoringgroups(self, request, pk=None):
        """Retrieve the tutoring groups of a tutor."""
        tutor = self.get_object()
        tutoring_groups = tutor.tutoring_groups.all()
        serializer = TutoringGroupSerializer(tutoring_groups, many=True,
                                             context={'request': request})
        return Response(serializer.data)


class StudentViewSet(ProfileViewSet):
    """API endpoint that allows students to be viewed or edited."""

    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @detail_route()
    def tutoringgroup(self, request, pk=None):
        """Retrieve the tutoring group of a student."""
        student = self.get_object()
        tutoring_group = student.tutoring_group
        serializer = TutoringGroupSerializer(tutoring_group,
                                             context={'request': request})
        return Response(serializer.data)


class SchoolStaffMemberViewSet(ProfileViewSet):
    """API endpoint that allows school staff members to be viewed or edited."""

    queryset = SchoolStaffMember.objects.all()
    serializer_class = SchoolStaffMembersSerializer
