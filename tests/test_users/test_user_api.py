"""Users API tests."""

from rest_framework import status

from tests.utils.api import HyperlinkedAPITestCase
from users.factory import UserFactory
from users.serializers import UserSerializer


class UserEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the users endpoints."""

    factory = UserFactory
    serializer_class = UserSerializer

    def perform_list(self):
        response = self.client.get('/api/users/')
        return response

    def test_list(self):
        self.assertRequiresAuth(
            self.perform_list,
            expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        response = self.client.get('/api/users/{obj.pk}/'.format(obj=obj))
        return response

    def test_retrieve(self):
        self.assertRequiresAuth(
            self.perform_retrieve,
            expected_status_code=status.HTTP_200_OK)
