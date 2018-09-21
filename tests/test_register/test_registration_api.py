"""Registration API tests."""

from django.contrib.auth import get_user_model
from rest_framework import status
from tests.utils import SimpleAPITestCase

from profiles.models import Student
from register.factory import RegistrationFactory
from register.models import Registration
from register.serializers import RegistrationSerializer
from users.factory import UserFactory

User = get_user_model()


class RegistrationReadTest(SimpleAPITestCase):
    """Test the read-only endpoints to registrations."""

    factory = RegistrationFactory
    list_url = '/api/registrations/'

    def setUp(self):
        self.factory.create_batch(3)

    def perform_list(self):
        response = self.client.get(self.list_url)
        return response

    def test_list_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_list,
            user=None,
            expected_status_code=status.HTTP_200_OK)


class RegistrationCreateTest(SimpleAPITestCase):
    """Test the creation of registrations.

    There is some complex logic which requires a few dedicated tests.
    """

    factory = RegistrationFactory
    serializer_class = RegistrationSerializer

    create_url = '/api/registrations/'

    def serialize(self, obj):
        serializer = self.serializer_class(obj)
        return serializer.data

    def get_create_data(self, obj=None):
        if obj is None:
            obj = self.factory.build()
        data = self.serialize(obj)
        data['password'] = 'foo1234baz'
        data.pop('submitted')  # read-only
        return data

    def _create(self, data):
        return self.client.post(self.create_url, data, format='json')

    def test_create_simple(self):
        data = self.get_create_data()
        response = self._create(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         response.data)

    def test_user_and_student_created(self):
        data = self.get_create_data()
        email = data['email']

        response = self._create(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         response.data)

        obj = Registration.objects.get(pk=response.data['id'])
        user = User.objects.get(email=email)
        self.assertEqual(obj.student, Student.objects.get(user=user))

    def test_if_email_of_existing_user_returns_bad_request(self):
        user = UserFactory.create()
        data = self.get_create_data()
        data['email'] = user.email

        response = self._create(data)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, response.data)
        self.assertIn('email', response.data)
