"""Category API tests."""

from django.contrib.auth import get_user_model
from rest_framework import status

from core.factory import AddressFactory
from core.serializers import AddressSerializer
from register.factory import EmergencyContactFactory, RegistrationFactory
from register.models import Registration
from register.serializers import (EmergencyContactSerializer,
                                  RegistrationSerializer)
from tests.utils import SimpleAPITestCase
from tutoring.factory import SchoolFactory, TutoringGroupFactory
from users.factory import UserFactory
from users.models import Student

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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_and_student_created(self):
        data = self.get_create_data()
        email = data['email']

        response = self._create(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that address and emergency contact were set on registration
        pk = response.data['id']
        obj = Registration.objects.get(pk=pk)
        self.assertEqual(obj.address.line1, address.line1)
        self.assertEqual(obj.emergency_contact.first_name,
                         emergency_contact.first_name)

    def test_if_email_of_existing_user_returns_bad_request(self):
        user = UserFactory.create()

        data = self.get_create_data()
        data['email'] = user.email

        response = self._create(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_if_tutoring_group_then_school_required(self):
        tutoring_group = TutoringGroupFactory.create()

        data = self.get_create_data()
        data['tutoring_group'] = tutoring_group.pk

        response = self._create(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_if_tutoring_group_belongs_to_school_ok(self):
        school = SchoolFactory.create()
        tutoring_group = TutoringGroupFactory.create(school=school)

        data = self.get_create_data()
        data['tutoring_group'] = tutoring_group.pk
        data['school'] = school.pk

        response = self._create(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tutoring_group_must_belong_to_school(self):
        tutoring_group = TutoringGroupFactory.create()
        school = SchoolFactory.create()
        self.assertNotEqual(tutoring_group.school, school)

        data = self.get_create_data()
        data['tutoring_group'] = tutoring_group.pk
        data['school'] = school.pk

        response = self._create(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
