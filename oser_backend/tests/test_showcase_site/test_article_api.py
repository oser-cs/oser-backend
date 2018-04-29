"""Article API tests."""

from time import sleep
from django.test import TestCase

from showcase_site.models import Article
from showcase_site.factory import ArticleFactory, CategoryFactory
from showcase_site.serializers import ArticleSerializer
from tests.utils import SimpleAPITestCase
from tests.utils import SimpleReadOnlyResourceTestMixin
from tests.utils import SerializerTestCaseMixin


class ArticleEndpointsTest(
        SimpleReadOnlyResourceTestMixin, SimpleAPITestCase):
    """Test access to the articles endpoints."""

    factory = ArticleFactory
    serializer_class = ArticleSerializer

    list_url = '/api/articles/'
    retrieve_url_fmt = '/api/articles/{obj.slug}/'
    retrieve_kwargs = {'active': True}

    @classmethod
    def setUpTestData(cls):
        cls.factory.create_batch(5)

    def test_only_active_articles_listed(self):
        response = self.perform_list()
        self.assertEqual(response.status_code, 200)
        for article_data in response.data:
            article = Article.objects.get(pk=article_data['id'])
            self.assertTrue(article.active)


class TestArticleSerializer(SerializerTestCaseMixin, TestCase):
    """Test the Article serializer."""

    serializer_class = ArticleSerializer
    factory_class = ArticleFactory

    expected_fields = (
        'id', 'title', 'slug', 'content', 'introduction',
        'published', 'modified',
        'image', 'display_image', 'pinned', 'categories', 'url',
    )

    def get_object(self):
        obj = super().get_object()
        for category in CategoryFactory.create_batch(3):
            if category not in obj.categories.all():
                obj.categories.add(category)
        obj.save()
        return obj

    def test_slug_is_read_only(self):
        self.assertTrue(self.serializer.fields['slug'].read_only)

    def test_contains_categories_titles(self):
        """Test the ArticleSerializer's `categories` field.

        It is an instance of CategoryField and converts the article's
        categories objects to a list of their titles.
        """
        expected = set(self.serializer.data['categories'])
        actual = set(c.title for c in self.obj.categories.all())
        self.assertEqual(actual, expected)

    def test_modified_only_contained_if_was_modified(self):
        obj = self.get_object()
        self.assertIsNone(self.serializer.data['modified'])
        sleep(1)
        obj.save()
        serializer = self.get_serializer(obj)
        self.assertIsNotNone(serializer.data['modified'])
