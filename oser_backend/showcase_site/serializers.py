"""Showcase site API serializers."""

from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Article.

    Suited for: list, retrieve, update, partial_update, delete
    """

    class Meta:  # noqa
        model = Article
        fields = ('id', 'url', 'title', 'content', 'published', 'image',
                  'pinned',)
        extra_kwargs = {
            'url': {'view_name': 'api:article-detail'},
        }
