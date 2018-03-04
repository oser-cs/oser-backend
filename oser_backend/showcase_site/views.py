"""Showcase site views."""
from rest_framework import viewsets
from dry_rest_permissions.generics import DRYPermissions

from .serializers import ArticleSerializer
from .serializers import CategorySerializer
from .serializers import TestimonySerializer
from .serializers import KeyFigureSerializer
from .serializers import PartnerSerializer
from .models import Article
from .models import Category
from .models import Testimony
from .models import KeyFigure
from .models import Partner

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


class TestimonyViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint to view testimonies.

    Actions: list, retrieve
    """

    serializer_class = TestimonySerializer
    queryset = Testimony.objects.all()


class KeyFigureViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint to view key figures.

    Actions: list, retrieve
    """

    serializer_class = KeyFigureSerializer
    queryset = KeyFigure.objects.all()


class PartnerViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint to view partners.

    Actions: list, retrieve
    """

    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()
