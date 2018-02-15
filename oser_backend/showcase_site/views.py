"""Showcase site views."""
from rest_framework.viewsets import ModelViewSet
from dry_rest_permissions.generics import DRYPermissions

from .serializers import ArticleSerializer
from .models import Article

# Create your views here.


class ArticleViewSet(ModelViewSet):
    """API endpoint that allows articles to be viewed or edited.

    Actions: list, retrieve, create, update, partial_update, destroy
    """
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = (DRYPermissions,)
