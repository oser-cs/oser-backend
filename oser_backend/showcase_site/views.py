"""Showcase site views."""
from rest_framework import viewsets

from .serializers import ArticleSerializer
from .serializers import CategorySerializer
from .serializers import TestimonySerializer
from .serializers import KeyFigureSerializer
from .serializers import PartnerSerializer
from .serializers import ActionSerializer
from .models import Article
from .models import Category
from .models import Testimony
from .models import KeyFigure
from .models import Partner
from .models import Action

# Create your views here.


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows articles to be viewed.

    Only active articles are visible in the API.

    Actions: list, retrieve
    """

    serializer_class = ArticleSerializer
    queryset = Article.objects.filter(active=True)


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

    Only active partners are visible in the API.

    Actions: list, retrieve
    """

    serializer_class = PartnerSerializer
    queryset = Partner.objects.filter(active=True)


class ActionViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint to view actions."""

    serializer_class = ActionSerializer
    queryset = Action.objects.all()
