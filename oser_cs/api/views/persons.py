"""Persons API views."""

from rest_framework import viewsets

from persons.models import Tutor
from api.serializers.persons import TutorSerializer

# Create your views here.


class TutorViewSet(viewsets.ReadOnlyModelViewSet):
    """List and detail views for tutors."""

    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
