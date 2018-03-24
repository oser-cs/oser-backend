from rest_framework import serializers
from .models import Document
from core.markdown import MarkdownField


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for documents."""

    content = MarkdownField()

    class Meta:  # noqa
        model = Document
        fields = ('url', 'title', 'slug', 'content')
        extra_kwargs = {
            # 'slug': {'read_only': True},
            'url': {
                'view_name': 'api:document-detail',
                'lookup_field': 'slug',
            },
        }
