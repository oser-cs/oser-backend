"""Users tests."""
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from users.models import User
from tests.utils import MyTestCase


class UserTest(MyTestCase):
    """Unit tests for the customized User model."""

    @classmethod
    def setUpTestData(self):
        self.obj = User.objects.create(username='johndoe')

    def test_gender_field_label(self):
        self.assertFieldVerboseName(User, 'gender', 'sexe')

    def test_gender_choices(self):
        self.assertTupleEqual(User._meta.get_field('gender').choices,
                              (('M', 'masculin'), ('F', 'féminin')))

    def test_gender_max_length(self):
        self.assertMaxLength(User, 'gender', 1)

    def test_phone_number_field_label(self):
        self.assertFieldVerboseName(User, 'phone_number', 'téléphone')

    # TODO add phone number validation tests
