"""Registration API tests."""

from django.contrib.auth import get_user_model
from rest_framework import status
from tests.utils import SimpleAPITestCase

from core.factory import AddressFactory
from core.serializers import AddressSerializer
from profiles.models import Student
from register.factory import EmergencyContactFactory, RegistrationFactory
from register.models import Registration
from register.serializers import (EmergencyContactSerializer,
                                  RegistrationSerializer)
from tutoring.factory import SchoolFactory, TutoringGroupFactory
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

    def test_create_with_address_and_emergency_contact(self):
        data = self.get_create_data()
        address = AddressFactory.build()
        emergency_contact = EmergencyContactFactory.build()
        data['address'] = AddressSerializer(address).data
        data['emergency_contact'] = EmergencyContactSerializer(
            emergency_contact).data

        response = self._create(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         response.data)

        # Verify that address and emergency contact were set on registration
        pk = response.data['id']
        obj = Registration.objects.get(pk=pk)
        self.assertEqual(obj.address.line1, address.line1)
        self.assertEqual(obj.emergency_contact.first_name,
                         emergency_contact.first_name)

    def test_create_with_school(self):
        school = SchoolFactory.create()
        data = self.get_create_data()
        data['school'] = school.pk

        response = self._create(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         response.data)

        # Verify that school was set on registration and student
        pk = response.data['id']
        obj = Registration.objects.get(pk=pk)
        self.assertEqual(obj.school.pk, school.pk)
        self.assertEqual(obj.student.school.pk, school.pk)

    def test_if_email_of_existing_user_returns_bad_request(self):
        user = UserFactory.create()
        data = self.get_create_data()
        data['email'] = user.email

        response = self._create(data)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, response.data)
        self.assertIn('email', response.data)
