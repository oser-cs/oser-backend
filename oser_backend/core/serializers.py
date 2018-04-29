"""Core serializers."""

from rest_framework import serializers

from core.markdown import MarkdownField
from django_countries.serializer_fields import CountryField

from .models import Address, Document


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for documents."""

    content = MarkdownField()

    class Meta:  # noqa
        model = Document
        fields = ('title', 'slug', 'content', 'url')
        extra_kwargs = {
            'url': {
                'view_name': 'api:document-detail',
                'lookup_field': 'slug',
            },
        }


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for addresses."""

    country = CountryField(
        country_dict=True,  # output country code and name
    )

    class Meta:  # noqa
        model = Address
        fields = ('line1', 'line2', 'post_code', 'city', 'country')
