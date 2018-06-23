"""Dynamic forms views and API endpoints."""

from django.http import HttpResponse
from rest_framework import mixins, viewsets

from .exports import write_zip
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


def download_multiple_forms_entries(request, forms):
    """Download form entries in a ZIP file containing CSV files.

    Note: this is not a proper Django view as it expects an iterable of
    Form objects (typically a queryset).
    """
    stream = write_zip(forms=forms, folder='reponses')
    stream.seek(0)
    contents = stream.read()
    filename = 'responses.zip'

    response = HttpResponse(contents,
                            content_type='application/x-zip-compressed')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response
