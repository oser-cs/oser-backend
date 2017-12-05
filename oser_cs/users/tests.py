"""Users tests."""

from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from tests.utils import random_email


User = get_user_model()


class UserTest(TestCase):
    """Unit tests for the customized User model."""

    @classmethod
    def setUpTestData(self):
        self.obj = User.objects.create(email=random_email())

    def test_gender_field_label(self):
        self.assertEqual(User._meta.get_field('gender').verbose_name, 'sexe')

    def test_gender_choices(self):
        self.assertTupleEqual(User._meta.get_field('gender').choices,
                              (('M', 'masculin'), ('F', 'féminin')))

    def test_gender_max_length(self):
        self.assertEqual(User._meta.get_field('gender').max_length, 1)

    def test_phone_number_field_label(self):
        self.assertEqual(User._meta.get_field('phone_number').verbose_name,
                         'téléphone')

    def test_get_absolute_url(self):
        response = self.client.get(f'/api/users/{self.obj.id}', follow=True)
        self.assertEqual(200, response.status_code)

    # TODO add phone number validation tests


class EmailAuthenticationTest(TestCase):
    """Test the custom email authentication backend."""

    def test_authenticate_with_email(self):
        user = User.objects.create(email='john.doe@email.net')
        user.set_password('secret')
        user.save()
        logged_in = self.client.login(username='john.doe@email.net',
                                      password='secret')
        self.assertTrue(logged_in)

    def test_username_not_unique(self):
        self.assertFalse(User._meta.get_field('username').unique)
        User.objects.create(email=random_email())

    def test_username_blank(self):
        self.assertTrue(User._meta.get_field('username').blank)

    def test_email_is_unique(self):
        self.assertTrue(User._meta.get_field('email').unique)

    def test_two_users_with_same_email_not_allowed(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(email='same.email@example.net')
            User.objects.create(email='same.email@example.net')

    def test_email_not_blank(self):
        self.assertFalse(User._meta.get_field('email').blank)
