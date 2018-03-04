"""Core views."""

from rest_framework import viewsets
from .serializers import LinkSerializer
from .models import Link

# Create your views here.


class LinkViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows links to be viewed.

    Actions: list, retrieve
    """

    serializer_class = LinkSerializer
    queryset = Link.objects.all()
