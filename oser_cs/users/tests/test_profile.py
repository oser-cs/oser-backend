"""Profile model tests."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import FieldDoesNotExist

from users.models import Profile, Student

from tests.utils import random_email, ModelTestCase


User = get_user_model()


class TestProfile(ModelTestCase):
    """Test case for the generic Profile model."""

    model = Profile
    field_tests = {
        'user': {
            'verbose_name': 'utilisateur',
        },
        'phone_number': {
            'verbose_name': 'téléphone',
            'max_length': 12,
        },
        'date_of_birth': {
            'verbose_name': 'date de naissance',
        },
    }

    @classmethod
    def setUpTestData(self):
        user = User.objects.create(email=random_email())
        self.obj = self.model.objects.create(user=user)

    def test_one_to_one_relationship(self):
        user = User.objects.get()
        self.assertEqual(user, self.obj.user)
        self.assertEqual(user.profile_object, self.obj)


class TestProfileTypes(TestCase):
    """Test the profile types API."""

    def test_user_account_field_choices(self):
        choices = User._meta.get_field('profile_type').choices
        self.assertEqual(choices, Profile.get_profile_types())

    def test_get_model_from_profile_type(self):
        model = Profile.get_model('student')
        self.assertEqual(model, Student)

    def test_profile_types(self):
        profile_types = Profile.get_profile_types()
        self.assertTupleEqual(profile_types, (
            ('student', 'Lycéen'),
            ('tutor', 'Tuteur'),
            ('schoolstaffmember', 'Personnel de lycée'),
        ))

    def test_generic_profile_not_in_profile_types(self):
        self.assertNotIn('profile', Profile.get_profile_types())
        self.assertNotIn('Profile', Profile.get_profile_types())


class TestUserProfileSignal(TestCase):
    """Test a new user instance gets a profile based on the profile_type."""

    def test_create_profile_for_user(self):
        User.objects.create(
            first_name='Adam',
            last_name='Smith',
            email='adam.smith@example.net',
            profile_type='student',
        )
        user = User.objects.get()
        self.assertIsInstance(user.profile, Student)
        self.assertNotIsInstance(user.profile_object, Student)


class ProfilePrimaryKeyIsUserTest(TestCase):
    """Test that Profile has its primary key as the user id."""

    @classmethod
    def setUpTestData(cls):
        # create a student
        cls.ua2 = User.objects.create(
            first_name='Adam',
            last_name='Smith',
            email='adam.smith@example.net',
            profile_type='student',
        )
        cls.s = cls.ua2.profile
        cls.s.date_of_birth = '2000-01-03'
        cls.s.address = '3 Rue de la vieille poissonnerie, 93100 Montreuil'

    def test_account_field(self):
        self.assertEqual(self.s.user, self.ua2)

    def test_account_id_field(self):
        self.assertEqual(self.s.user_id, self.ua2.id)

    def test_account_id_is_pk(self):
        self.assertEqual(self.s.user_id, self.s.pk)

    def test_no_proper_id_field(self):
        with self.assertRaises(FieldDoesNotExist):
            self.s._meta.get_field('id')

    def test_id_with_property(self):
        self.assertEqual(self.s.id, self.s.user_id)

    def test_reverse_on_user_account(self):
        self.assertEqual(self.ua2.profile, self.s)
