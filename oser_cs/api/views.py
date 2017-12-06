"""API views."""

from rest_framework import viewsets

from users.models import User
from persons.models import Tutor
from tutoring.models import TutoringGroup
from .serializers import (
    UserSerializer, TutorSerializer, TutoringGroupSerializer
)

# Create your views here.


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """List and detail views for users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class TutorViewSet(viewsets.ReadOnlyModelViewSet):
    """List and detail views for tutors."""

    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer


class TutoringGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """List and detail views for tutoring groups."""

    queryset = TutoringGroup.objects.all()
    serializer_class = TutoringGroupSerializer
