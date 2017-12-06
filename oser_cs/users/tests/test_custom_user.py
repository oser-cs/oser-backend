"""Users tests."""
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from tests.utils import random_email, FieldTestCase


User = get_user_model()


class UserTest(TestCase):
    """Unit tests for the customized User model."""

    @classmethod
    def setUpTestData(self):
        self.obj = User.objects.create(email=random_email())

    # date_of_birth field

    def test_date_of_birth_field_label(self):
        self.assertEqual(User._meta.get_field('date_of_birth').verbose_name,
                         'date de naissance')

    # gender field

    def test_gender_field_label(self):
        self.assertEqual(User._meta.get_field('gender').verbose_name, 'sexe')

    def test_gender_choices(self):
        self.assertTupleEqual(User._meta.get_field('gender').choices,
                              (('M', 'Homme'), ('F', 'Femme')))

    def test_gender_max_length(self):
        self.assertEqual(User._meta.get_field('gender').max_length, 1)

    def test_gender_default(self):
        field = User._meta.get_field('gender')
        self.assertEqual(User.MALE, field.default)
        self.assertFalse(field.null)

    # phone_number field

    def test_phone_number_field_label(self):
        self.assertEqual(User._meta.get_field('phone_number').verbose_name,
                         'téléphone')

    def test_phone_number_is_blank_and_nullable(self):
        field = User._meta.get_field('phone_number')
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    # url

    def test_get_absolute_url(self):
        response = self.client.get(f'/api/users/{self.obj.id}', follow=True)
        self.assertEqual(200, response.status_code)

    # TODO add phone number validation tests


class EmailAuthenticationTest(TestCase):
    """Tests to make sure a user can authenticate with email and password."""

    def test_authenticate_with_email_succeeds(self):
        email, password = 'john.doe@email.net', 'secretpassword'
        user = User.objects.create(email=email)
        user.set_password(password)
        user.save()
        logged_in = self.client.login(email=email, password=password)
        self.assertTrue(logged_in)

    def test_authenticate_with_username_fails(self):
        username = 'johndoe'
        email, password = 'john.doe@email.net', 'secretpassword'
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        logged_in = self.client.login(username=username, password=password)
        self.assertFalse(logged_in)


class UserUsernameFieldTest(FieldTestCase):
    """Test the User.username field.

    The email authentication system must have released the imperative
    of having username unique and non-nullable.
    """

    model = User
    field_name = 'username'
    tests = {
        'unique': False,
        'blank': True,
        'null': True,
    }

    def test_two_users_with_same_username_allowed(self):
        self.model.objects.create(email=random_email())
        self.model.objects.create(email=random_email())


class UserEmailFieldTest(FieldTestCase):
    """Test the User.email field.

    The email authentication system must have made the email unique and
    non-nullable from a database point of view.
    """

    model = User
    field_name = 'email'
    tests = {
        'unique': True,
        'blank': False,
        'null': False,
    }

    def test_two_users_with_same_email_not_allowed(self):
        with self.assertRaises(IntegrityError):
            self.model.objects.create(email='same.email@example.net')
            self.model.objects.create(email='same.email@example.net')
