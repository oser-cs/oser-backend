"""Core views."""

from django.shortcuts import get_object_or_404
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """API routes that allow to retrieve a document."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    lookup_field = 'slug'
