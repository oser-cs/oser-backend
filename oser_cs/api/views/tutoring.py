"""Tutoring API views."""

from rest_framework import viewsets
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin,
)

from tutoring.models import TutoringGroup, School, TutoringSession
from api.serializers.tutoring import (
    TutoringGroupSerializer, SchoolSerializer, TutoringSessionSerializer,
)

# Create your views here.


class TutoringGroupViewSet(ListModelMixin,
                           RetrieveModelMixin,
                           CreateModelMixin,
                           viewsets.GenericViewSet):
    """API endpoint that allows tutoring groups to be viewed or edited.

    retrieve:
    Return a tutoring group instance.

    list:
    Return all tutoring groups.

    create:
    Create a tutoring group instance.
    """

    queryset = TutoringGroup.objects.all()
    serializer_class = TutoringGroupSerializer


class SchoolViewSet(ListModelMixin,
                    RetrieveModelMixin,
                    CreateModelMixin,
                    viewsets.GenericViewSet):
    """API endpoint that allows schools to be viewed or edited.

    retrieve:
    Return a school instance.

    list:
    Return all schools.

    create:
    Create a school instance.
    """

    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class TutoringSessionViewSet(ListModelMixin,
                             RetrieveModelMixin,
                             CreateModelMixin,
                             viewsets.GenericViewSet):
    """API endpoint that allows tutoring sessions to be viewed or edited.

    retrieve:
    Return a tutoring session instance.

    list:
    Return all tutoring sessions.

    create:
    Create a tutoring session instance.
    """

    queryset = TutoringSession.objects.all()
    serializer_class = TutoringSessionSerializer
