"""Article API tests."""

from rest_framework import status
from tests.factory import ArticleFactory
from tests.utils.api import HyperlinkedAPITestCase

from showcase_site.serializers import ArticleSerializer


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

    def perform_create(self):
        url = '/api/articles/'
        obj = self.factory.build()
        data = self.serialize(obj, 'post', url)
        response = self.client.post(url, data, format='json')
        return response

    def test_create_requires_to_be_authenticated(self):
        self.assertRequiresAuth(
            self.perform_create,
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
