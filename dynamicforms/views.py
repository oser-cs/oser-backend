"""Dynamic forms views and API endpoints."""

from rest_framework import mixins, viewsets

from .models import Form, FormEntry
from .serializers import (FormDetailSerializer, FormEntrySerializer,
                          FormSerializer)


class FormViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve forms."""

    serializer_class = FormSerializer
    queryset = Form.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FormDetailSerializer
        return FormSerializer


class FormEntryViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Create form entries."""

    serializer_class = FormEntrySerializer
    queryset = FormEntry.objects.all()
