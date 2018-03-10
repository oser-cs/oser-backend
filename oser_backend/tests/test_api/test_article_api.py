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

    create_url = '/api/articles/'

    def get_create_data(self):
        # Use .build() instead of .create() to get a raw object
        # not stored in DB.
        obj = self.factory.build()
        data = self.serialize(obj, 'post', self.create_url)
        return data

    def perform_create(self, data=None):
        if data is None:
            data = self.get_create_data()
        response = self.client.post(self.create_url, data, format='json')
        return response

    def test_create_requires_to_be_authenticated(self):
        self.assertRequiresAuth(
            self.perform_create,
            expected_status_code=status.HTTP_201_CREATED)

    def test_create_with_categories(self):
        # create categories
        categories = CategoryFactory.create_batch(3)
        data = self.get_create_data()
        # add categories titles to the POST data
        for cat in categories:
            data.setdefault('categories', []).append(cat.title)

        self.assertUserRequestResponse(
            lambda: self.perform_create(data=data),
            expected_status_code=status.HTTP_201_CREATED)

    def perform_update(self):
        obj = self.factory.create()
        url = '/api/articles/{obj.pk}/'.format(obj=obj)
        data = self.serialize(obj, 'put', url)
        data['pinned'] = not data['pinned']
        response = self.client.put(url, data, format='json')
        return response

    def test_update_requires_to_be_authenticated(self):
        self.assertRequiresAuth(
            self.perform_update,
            expected_status_code=status.HTTP_200_OK)

    def perform_partial_update(self):
        obj = self.factory.create()
        url = '/api/articles/{obj.pk}/'.format(obj=obj)
        data = {'pinned': not obj.pinned}
        response = self.client.patch(url, data, format='json')
        return response

    def test_partial_update_requires_to_be_authenticated(self):
        self.assertRequiresAuth(
            self.perform_partial_update,
            expected_status_code=status.HTTP_200_OK)

    def perform_delete(self):
        obj = self.factory.create()
        url = '/api/articles/{obj.pk}/'.format(obj=obj)
        response = self.client.delete(url)
        return response

    def test_delete_requires_to_be_authenticated(self):
        self.assertRequiresAuth(
            self.perform_delete,
            expected_status_code=status.HTTP_204_NO_CONTENT)


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
