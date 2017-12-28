"""Users API tests."""

from rest_framework import status

from users.serializers import UserSerializer, UserCreateSerializer
from tests.factory import UserFactory
from tests.utils.api import HyperlinkedAPITestCase


class UserEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the users endpoints."""

    factory = UserFactory
    serializer_class = UserSerializer

    def perform_list(self):
        response = self.client.get('/api/users/')
        return response

    def test_list_anonymous_is_forbidden(self):
        """Test anonymous user cannot list users."""
        self.assertForbidden(self.perform_list, user=None)

    def test_list_authenticated_is_allowed(self):
        """Test that authenticated user can list users."""
        self.assertAuthorized(self.perform_list, user=UserFactory.create(),
                              expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        response = self.client.get(f'/api/users/{obj.pk}/')
        return response

    def test_retrieve_anonymous_is_forbidden(self):
        """Test that visitors cannot retrieve a user."""
        self.assertForbidden(self.perform_retrieve, user=None)

    def test_retrieve_authenticated_is_allowed(self):
        """Test that authenticated users can retrive a user."""
        self.assertAuthorized(self.perform_retrieve, user=UserFactory.create(),
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
        self.assertAuthorized(self.perform_create, user=None,
                              expected_status_code=status.HTTP_201_CREATED)

    def perform_update(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = f'/api/users/{obj.pk}/'
        data = self.serialize(obj, 'put', url)
        data['first_name'] = 'Modified first name'
        response = self.client.put(url, data, format='json')
        return response

    def test_update_anonymous_is_forbidden(self):
        self.assertForbidden(self.perform_update, user=None)

    def test_update_authenticated_is_forbidden(self):
        self.assertForbidden(self.perform_update, user=UserFactory.create())

    def test_update_authenticated_self_is_allowed(self):
        user = UserFactory.create()
        self.assertAuthorized(lambda: self.perform_update(obj=user),
                              user=user,
                              expected_status_code=status.HTTP_200_OK)

    def perform_partial_update(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        response = self.client.patch(f'/api/users/{obj.pk}/',
                                     data={'first_name': 'Some first name'},
                                     format='json')
        return response

    def test_partial_update_anonymous_is_forbidden(self):
        self.assertForbidden(self.perform_partial_update, user=None)

    def test_partial_update_authenticated_is_forbidden(self):
        self.assertForbidden(self.perform_partial_update,
                             user=UserFactory.create())

    def test_partial_update_authenticated_self_is_allowed(self):
        user = UserFactory.create()
        self.assertAuthorized(lambda: self.perform_partial_update(obj=user),
                              user=user,
                              expected_status_code=status.HTTP_200_OK)

    def perform_delete(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        response = self.client.delete(f'/api/users/{obj.pk}/')
        return response

    def test_delete_anonymous_is_forbidden(self):
        self.assertForbidden(self.perform_delete, user=None)

    def test_delete_authenticated_is_forbidden(self):
        self.assertForbidden(self.perform_delete, user=UserFactory.create())

    def test_delete_authenticated_self_is_forbidden(self):
        user = UserFactory.create()
        self.assertAuthorized(lambda: self.perform_delete(obj=user),
                              user=user,
                              expected_status_code=status.HTTP_204_NO_CONTENT)
