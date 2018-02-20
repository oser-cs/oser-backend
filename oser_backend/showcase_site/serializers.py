"""Showcase site API serializers."""

from rest_framework import serializers
from .models import Article, Category, Testimony, KeyFigure


class CategoryField(serializers.RelatedField):
    """Custom field to allow read/write of category using its title.

    See
    ---
    http://www.django-rest-framework.org/api-guide/relations/#custom-relational-fields
    """

    def to_representation(self, obj):
        """Object instance -> JSON-compatible representation"""
        return obj.title

    def to_internal_value(self, data):
        """Object instance <- JSON-compatible representation"""
        category = Category.objects.get(title=data)
        return category

    def get_queryset(self):
        """Define default queryset to be all categories.

        Allows to skip passing queryset=... when creating a CategoryField.
        """
        return Category.objects.all()


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category."""

    class Meta:  # noqa
        model = Category
        fields = ('id', 'title', 'articles_count')


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Article.

    Suited for: list, retrieve, update, partial_update, delete
    """

    categories = CategoryField(many=True, required=False)

    class Meta:  # noqa
        model = Article
        fields = ('id', 'url', 'title', 'slug',
                  'content', 'published', 'image',
                  'pinned', 'categories',)
        extra_kwargs = {
            'slug': {'read_only': True},
            'url': {'view_name': 'api:article-detail'},
        }


class TestimonySerializer(serializers.ModelSerializer):
    """Serializer for Testimony."""

    class Meta:  # noqa
        model = Testimony
        fields = ('id', 'author', 'created', 'content',)


class KeyFigureSerializer(serializers.ModelSerializer):
    """Serializer for KeyFigure."""

    class Meta:  # noqa
        model = KeyFigure
        fields = ('order', 'figure', 'description',)
