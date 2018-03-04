"""Core API serializers."""

from rest_framework import serializers
from .models import Link


class LinkSerializer(serializers.ModelSerializer):
    """Serializer for Link."""

    class Meta:  # noqa
        model = Link
        fields = ('slug', 'url')
