"""Persons API views."""

from rest_framework import viewsets
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin,
)

from persons.models import Tutor, Student
from api.serializers.persons import TutorSerializer, StudentSerializer

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
