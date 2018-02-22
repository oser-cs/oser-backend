"""Visits serializers."""

from rest_framework import serializers
from .models import Visit


class VisitSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Visit."""

    class Meta:  # noqa
        model = Visit
        fields = ('id', 'url', 'title', 'summary', 'description',
                  'place', 'date', 'deadline',
                  'registrations_open',
                  'image', 'fact_sheet',)
        extra_kwargs = {
            'url': {'view_name': 'api:visit-detail'},
        }
