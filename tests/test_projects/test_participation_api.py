"""Projects participations API tests."""

from rest_framework import status
from tests.utils import SimpleAPITestCase, logged_in

from projects.factory import EditionFactory, ParticipationFactory
from users.factory import UserFactory
from dynamicforms.models import Form


class ParticipationReadTest(SimpleAPITestCase):
    """Test access to the editions read endpoints."""

    factory = ParticipationFactory

    read_expected_fields = {'id', 'user', 'edition',
                            'state', 'submitted'}

    def setUp(self):
        self.factory.create_batch(3)

    def perform_list(self):
        url = '/api/project-participations/'
        response = self.client.get(url)
        return response

    def perform_retrieve(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = '/api/project-participations/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_list_requires_authentication(self):
        self.assertRequiresAuth(
            self.perform_list, expected_status_code=status.HTTP_200_OK)

    @logged_in
    def test_list_returns_expected_fields(self):
        response = self.perform_list()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fields = set(response.data[0])
        self.assertSetEqual(fields, self.read_expected_fields)

    def test_retrieve_requires_authentication(self):
        self.assertRequiresAuth(
            self.perform_retrieve, expected_status_code=status.HTTP_200_OK)

    @logged_in
    def test_retrieve_returns_expected_fields(self):
        response = self.perform_retrieve()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fields = set(response.data)
        self.assertSetEqual(fields, self.read_expected_fields)


class ParticipationCreateTest(SimpleAPITestCase):

    def perform_create(self):
        user = UserFactory.create()
        edition = EditionFactory.create()
        form = Form.objects.create(title="What's up?")
        entry = {
            'form': form.pk,
            'answers': [],
        }
        payload = {
            'user': user.pk,
            'edition': edition.pk,
            'entry': entry,
        }
        return self.client.post('/api/project-participations/',
                                data=payload, format='json')

    def test_create_requires_authentication(self):
        self.assertRequiresAuth(
            self.perform_create, expected_status_code=status.HTTP_201_CREATED)

    @logged_in
    def test_returns_expected_fields(self):
        response = self.perform_create()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected = {'id', 'user', 'edition', 'state', 'submitted'}
        self.assertSetEqual(expected, set(response.data))
