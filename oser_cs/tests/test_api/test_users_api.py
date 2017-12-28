"""Users API tests."""

from rest_framework import status
from tests.factory import UserFactory
from tests.utils.api import HyperlinkedAPITestCase

from users.serializers import UserCreateSerializer, UserSerializer


class UserEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the users endpoints."""

    factory = UserFactory
    serializer_class = UserSerializer

    def perform_list(self):
        response = self.client.get('/api/users/')
        return response

    def test_list_requires_authentication(self):
        self.assertRequiresAuth(self.perform_list,
                                expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        response = self.client.get('/api/users/{obj.pk}/'.format(obj=obj))
        return response

    def test_retrieve_requires_authentication(self):
        self.assertRequiresAuth(self.perform_retrieve,
                                expected_status_code=status.HTTP_200_OK)

    def perform_create(self):
        url = '/api/users/'
        obj = self.factory.build()
        data = self.serialize(obj, 'post', url,
                              serializer_class=UserCreateSerializer)
        data['password'] = 'secret'  # write-only on the serializer
        response = self.client.post(url, data, format='json')
        return response

    def test_create_anonymous_is_allowed(self):
        """Test that anyone can create a user.

        (Provided they are logged into the API.)
        """
        self.assertRequestResponse(
            self.perform_create, user=None,
            expected_status_code=status.HTTP_201_CREATED)

    def perform_update(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = '/api/users/{obj.pk}/'.format(obj=obj)
        data = self.serialize(obj, 'put', url)
        data['first_name'] = 'Modified first name'
        response = self.client.put(url, data, format='json')
        return response

    def test_update_requires_more_than_authentication(self):
        self.assertAuthForbidden(self.perform_update)

    def test_update_authenticated_self_is_allowed(self):
        user = UserFactory.create()
        self.assertRequestResponse(lambda: self.perform_update(obj=user),
                                   user=user,
                                   expected_status_code=status.HTTP_200_OK)

    def perform_partial_update(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        response = self.client.patch('/api/users/{obj.pk}/'.format(obj=obj),
                                     data={'first_name': 'Some first name'},
                                     format='json')
        return response

    def test_partial_update_requires_more_than_authentication(self):
        self.assertAuthForbidden(self.perform_partial_update)

    def test_partial_update_authenticated_self_is_allowed(self):
        user = UserFactory.create()
        self.assertRequestResponse(
            lambda: self.perform_partial_update(obj=user),
            user=user,
            expected_status_code=status.HTTP_200_OK)

    def perform_delete(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        response = self.client.delete('/api/users/{obj.pk}/'.format(obj=obj))
        return response

    def test_delete_requires_more_than_authentication(self):
        self.assertAuthForbidden(self.perform_delete)

    def test_delete_authenticated_self_is_forbidden(self):
        user = UserFactory.create()
        self.assertRequestResponse(
            lambda: self.perform_delete(obj=user),
            user=user,
            expected_status_code=status.HTTP_204_NO_CONTENT)
