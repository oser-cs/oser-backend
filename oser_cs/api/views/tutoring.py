"""Tutoring API views."""

from rest_framework import viewsets
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin,
)
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from tutoring.models import TutoringGroup, School, TutoringSession
from api.serializers.tutoring import (
    TutoringGroupSerializer,
    SchoolSerializer, SchoolCreateSerializer,
    TutoringSessionSerializer,
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
                    RetrieveUpdateDestroyAPIView,
                    CreateModelMixin,
                    viewsets.GenericViewSet):
    """API endpoint that allows schools to be viewed, edited or destroyed.

    list:
    Return all schools.

    retrieve:
    Return a school instance.

    create:
    Create a school instance.

    update:
    Update a school instance.

    destroy:
    Delete a school instance.
    """

    queryset = School.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return SchoolCreateSerializer
        return SchoolSerializer


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
