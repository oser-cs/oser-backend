"""Users API tests."""

from rest_framework import status

from users.serializers import UserSerializer, UserCreateSerializer
from tests.factory import UserFactory
from tests.utils.api import HyperlinkedAPITestCase


class UserEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the users endpoints."""

    factory = UserFactory
    serializer_class = UserSerializer

    def test_list(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        obj = self.factory.create()
        response = self.client.get(f'/api/users/{obj.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        url = '/api/users/'
        obj = self.factory.build()
        data = self.serialize(obj, 'post', url,
                              serializer_class=UserCreateSerializer)
        data['password'] = 'secret'  # write-only on the serializer
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         response.data)

    def test_update(self):
        obj = self.factory.create()
        url = f'/api/users/{obj.pk}/'
        data = self.serialize(obj, 'put', url)
        data['first_name'] = 'Modified first name'
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        obj = self.factory.create()
        response = self.client.patch(f'/api/users/{obj.pk}/',
                                     data={'first_name': 'Some first name'},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        obj = self.factory.create()
        response = self.client.delete(f'/api/users/{obj.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
