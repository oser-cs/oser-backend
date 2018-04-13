"""Category API tests."""

from rest_framework import status
from register.factory import RegistrationFactory
from register.serializers import RegistrationSerializer
from tests.utils import SimpleAPITestCase


class RegistrationEndpointsTest(SimpleAPITestCase):
    """Test access to the registrations endpoints."""

    factory = RegistrationFactory
    serializer_class = RegistrationSerializer

    list_url = '/api/registrations/'
    create_url = '/api/registrations/'

    def serialize(self, obj):
        serializer = self.serializer_class(obj)
        return serializer.data

    def perform_list(self):
        response = self.client.get(self.list_url)
        return response

    def test_list_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_list,
            user=None,
            expected_status_code=status.HTTP_200_OK)

    def perform_create(self):
        obj = self.factory.build()
        data = self.serialize(obj)
        data.pop('submitted')  # read-only
        response = self.client.post(self.create_url, data, format='json')
        return response

    def test_list_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_list,
            user=None,
            expected_status_code=status.HTTP_200_OK)

    def test_create_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_create,
            user=None,
            expected_status_code=status.HTTP_201_CREATED)
