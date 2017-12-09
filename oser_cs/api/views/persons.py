"""Persons API views."""

from rest_framework import viewsets
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin,
)

from persons.models import Tutor
from api.serializers.persons import TutorSerializer

# Create your views here.


class TutorViewSet(ListModelMixin,
                   RetrieveModelMixin,
                   CreateModelMixin,
                   viewsets.GenericViewSet):
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
