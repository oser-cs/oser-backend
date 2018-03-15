"""Test the authentication mechanism used by the API."""

from rest_framework import status
from rest_framework.test import APITestCase

from users.factory import UserFactory
from users.serializers import UserSerializer


class TestTokenAuth(APITestCase):
    """Test the Token authentication system.

    Note: the host (typically localhost:xxxx) is replaced by 'testserver'
    during a DRF test case.
    An external client would have to use the real host name.
    """

    def setUp(self):
        super().setUp()
        # create a fake user
        self.fake_password = 'pass'
        self.user = UserFactory.create(password=self.fake_password)

    def perform_get_token(self):
        post_data = {
            'username': self.user.email,
            'password': self.fake_password
        }
        response = self.client.post('/api/auth/get-token/', data=post_data)
        return response

    def test_get_token(self):
        """Test retrieving the auth token from email/password."""
        response = self.perform_get_token()
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         response.data)
        self.assertIn('token', response.json())
        token = response.json().get('token')
        self.assertIsNotNone(token)

    def test_response_contains_user(self):
        """Test response from auth token view also returns user."""
        response = self.perform_get_token()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = response.json().get('user')
        self.assertIsNotNone(user)
        # try to pass the returned user data through a UserSerializer
        serializer = UserSerializer(data=user)
        self.assertTrue(serializer.is_valid())

    def test_request_using_token(self):
        """Test once authenticated, the token can be used in the API."""
        token_response = self.perform_get_token()
        token = token_response.json().get('token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        # get some data using the token
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         response.data)
