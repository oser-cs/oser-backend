"""Article API tests."""

from django.test import TestCase
from rest_framework import status

from showcase_site.factory import ArticleFactory, CategoryFactory
from showcase_site.serializers import ArticleSerializer
from tests.utils import HyperlinkedAPITestCase, SerializerTestCaseMixin


class ArticleEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the articles endpoints."""

    factory = ArticleFactory
    serializer_class = ArticleSerializer

    def perform_list(self):
        url = '/api/articles/'
        response = self.client.get(url)
        return response

    def test_list_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_list,
            user=None,
            expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        url = '/api/articles/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_retrieve,
            user=None,
            expected_status_code=status.HTTP_200_OK)


class TestArticleSerializer(SerializerTestCaseMixin, TestCase):
    """Test the Article serializer."""

    serializer_class = ArticleSerializer
    factory_class = ArticleFactory

    expected_fields = (
        'id', 'url', 'title', 'slug', 'content', 'published', 'image',
        'pinned', 'categories'
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
