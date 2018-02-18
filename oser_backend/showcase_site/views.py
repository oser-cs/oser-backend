"""Showcase site views."""
from rest_framework import viewsets
from dry_rest_permissions.generics import DRYPermissions

from .serializers import ArticleSerializer, CategorySerializer
from .models import Article, Category

# Create your views here.


class ArticleViewSet(viewsets.ModelViewSet):
    """API endpoint that allows articles to be viewed or edited.

    Actions: list, retrieve, create, update, partial_update, destroy
    """
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = (DRYPermissions,)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows categories to be viewed.

    Actions: list, retrieve
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
