"""Projects views."""

from rest_framework import mixins, viewsets

from .models import Edition, Participation, Project
from .serializers import (EditionSerializer, ParticipationSerializer,
                          ProjectSerializer)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve projects."""

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class EditionViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve project editions."""

    queryset = Edition.objects.all()
    serializer_class = EditionSerializer


class ParticipationViewSet(mixins.CreateModelMixin,
                           viewsets.ReadOnlyModelViewSet):
    """Endpoints for manipulating participations to project editions."""

    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer
