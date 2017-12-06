"""Tutoring API views."""

from rest_framework import viewsets
from tutoring.models import TutoringGroup
from api.serializers.tutoring import TutoringGroupSerializer

# Create your views here.


class TutoringGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """List and detail views for tutoring groups."""

    queryset = TutoringGroup.objects.all()
    serializer_class = TutoringGroupSerializer
