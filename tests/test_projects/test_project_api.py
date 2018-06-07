"""Project API tests."""

from rest_framework import status
from tests.utils import SimpleAPITestCase, logged_in

from projects.factory import ProjectFactory


class ProjectEndpointsTest(SimpleAPITestCase):
    """Test access to the projects endpoints."""

    factory = ProjectFactory

    def setUp(self):
        self.factory.create_batch(3)

    def perform_list(self):
        url = '/api/projects/'
        response = self.client.get(url)
        return response

    def perform_retrieve(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = '/api/projects/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_list_requires_authentication(self):
        self.assertRequiresAuth(
            self.perform_list, expected_status_code=status.HTTP_200_OK)

    @logged_in
    def test_list_returns_expected_fields(self):
        expected = {'id', 'url', 'name', 'logo', 'description'}
        response = self.perform_list()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fields = set(response.data[0])
        self.assertSetEqual(fields, expected)

    def test_retrieve_requires_authentication(self):
        self.assertRequiresAuth(
            self.perform_retrieve, expected_status_code=status.HTTP_200_OK)

    @logged_in
    def test_retrieve_returns_expected_fields(self):
        expected = {'id', 'url', 'name', 'logo', 'description'}
        response = self.perform_retrieve()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fields = set(response.data)
        self.assertSetEqual(fields, expected)
