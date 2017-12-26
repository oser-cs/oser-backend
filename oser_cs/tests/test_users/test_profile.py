"""Profile model tests."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import FieldDoesNotExist

from users.models import Profile, Student
from tests.factory import UserFactory, ProfileFactory
from tests.utils import ModelTestCase


User = get_user_model()


class TestProfile(ModelTestCase):
    """Test case for the generic Profile model."""

    model = Profile
    field_tests = {
        'user': {
            'verbose_name': 'utilisateur',
            'primary_key': True,
        },
    }
    model_tests = {
        'verbose_name': 'profil',
    }

    def setUp(self):
        self.obj = ProfileFactory.create(user__first_name='Bob',
                                         user__last_name='Dylan')

    def test_one_to_one_relationship(self):
        user = User.objects.get()
        self.assertEqual(user, self.obj.user)
        # user.profile_object is the raw Profile object
        self.assertEqual(user.profile_object, self.obj)

    def test_full_name_property(self):
        self.assertEqual(self.obj.full_name, 'Bob Dylan')


class TestProfileTypes(TestCase):
    """Test the profile types API."""

    def test_user_profile_type_choices(self):
        choices = User._meta.get_field('profile_type').choices
        self.assertEqual(choices, Profile.get_profile_type_choices())

    def test_get_model_from_profile_type(self):
        model = Profile.get_model('student')
        self.assertEqual(model, Student)

    def test_profile_types(self):
        profile_types = Profile.get_profile_type_choices()
        self.assertTupleEqual(profile_types, (
            ('student', 'Lycéen'),
            ('tutor', 'Tuteur'),
            ('schoolstaffmember', 'Membre du personnel de lycée'),
        ))

    def test_generic_profile_not_in_profile_types(self):
        self.assertNotIn('profile', Profile.get_profile_type_choices())
        self.assertNotIn('Profile', Profile.get_profile_type_choices())


class TestCreateProfileForUserSignal(TestCase):
    """Test a new user instance gets a profile based on the profile_type."""

    def test_create_user_assigns_a_profile_according_to_profile_type(self):
        UserFactory.create(profile_type='student')
        # A signal was triggered and user received a Student profile
        user = User.objects.get()
        # user.profile is a property that dynamically finds the Profile
        # object corresponding to (profile.user == user)
        self.assertIsInstance(user.profile, Student)
        # The "raw" Profile object is accessible through user.profile_object
        self.assertIsInstance(user.profile_object, Profile)
        self.assertNotIsInstance(user.profile_object, Student)


class ProfilePrimaryKeyIsUserTest(TestCase):
    """Test that Profile has its primary key as the user id."""

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(profile_type='student')
        cls.student = cls.user.profile

    def test_profile_user_field(self):
        self.assertEqual(self.student.user, self.user)

    def test_profile_user_id_field(self):
        self.assertEqual(self.student.user_id, self.user.id)

    def test_profile_pk_is_user_id(self):
        self.assertEqual(self.student.pk, self.student.user_id)

    def test_profile_has_no_proper_id_field(self):
        with self.assertRaises(FieldDoesNotExist):
            self.student._meta.get_field('id')

    def test_profile_has_id_property(self):
        self.assertEqual(self.student.id, self.student.user_id)

    def test_reverse_relationship_on_user_object(self):
        self.assertEqual(self.user.profile, self.student)
