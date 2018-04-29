"""Showcase site API serializers."""

from rest_framework import serializers

from core.markdown import MarkdownField

from .models import Action, Article, Category, KeyFigure, Partner, Testimony


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

    content = MarkdownField()
    categories = CategoryField(many=True, required=False)
    modified = serializers.SerializerMethodField()

    def get_modified(self, obj: Article):
        """Only expose modified if article has already been modified."""
        return obj.was_modified and obj.modified or None

    class Meta:  # noqa
        model = Article
        fields = ('id', 'title', 'slug', 'introduction',
                  'content', 'published', 'modified', 'image',
                  'display_image', 'pinned', 'categories', 'url',)
        extra_kwargs = {
            'slug': {'read_only': True},
            'url': {'view_name': 'api:article-detail'},
        }


class TestimonySerializer(serializers.ModelSerializer):
    """Serializer for Testimony."""

    class Meta:  # noqa
        model = Testimony
        fields = ('id', 'source', 'created', 'quote',)


class KeyFigureSerializer(serializers.ModelSerializer):
    """Serializer for KeyFigure."""

    class Meta:  # noqa
        model = KeyFigure
        fields = ('order', 'figure', 'description',)


class PartnerSerializer(serializers.ModelSerializer):
    """Serializer for Partner."""

    class Meta:  # noqa
        model = Partner
        fields = ('id', 'name', 'website', 'logo', 'premium')


class ActionSerializer(serializers.ModelSerializer):
    """Serializer for action points."""

    class Meta:  # noqa
        model = Action
        fields = ('id', 'title', 'description', 'key_figure',
                  'thumbnail', 'highlight')
