"""Tutoring tests."""

from django.test import TestCase
from django.contrib.auth import get_user_model
import tutoring.models
from users.permissions import Groups
from users.models import Tutor
from utils import group_exists
from tests.utils import ModelTestCase, random_uai_code, random_email
from tests.factory import StudentFactory, TutoringGroupFactory

User = get_user_model()


class TutoringTest(TestCase):
    """General tests on the tutoring app."""

    def test_VP_TUTORAT_exists(self):
        self.assertTrue(group_exists(Groups.VP_TUTORAT))


class TutoringGroupTest(ModelTestCase):
    """Test the TutoringGroup model."""

    model = tutoring.models.TutoringGroup
    field_tests = {
        'name': {
            'verbose_name': 'nom',
            'max_length': 200,
        },
        'tutors': {
            'verbose_name': 'tuteurs',
            'blank': True,
        },
    }
    # TODO implement
    model_tests = {
        'verbose_name': 'groupe de tutorat',
        'verbose_name_plural': 'groupes de tutorat',
        'ordering': ('name',),
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = TutoringGroupFactory.create()

    def test_get_absolute_url(self):
        response = self.client.get(f'/api/tutoring/groups/{self.obj.pk}/')
        self.assertEqual(200, response.status_code)

    def test_tutors_many_to_many_relationship(self):
        user = User.objects.create(email=random_email())
        tutor = Tutor.objects.create(user=user)
        tutoring.models.TutorTutoringGroup.objects.create(
            tutoring_group=self.obj,
            tutor=tutor)
        self.assertIn(tutor, self.obj.tutors.all())
        self.assertIn(self.obj, tutor.tutoring_groups.all())


class TutoringGroupPermissionsTest(TestCase):
    """Test permissions on Tutoring Group."""

    @classmethod
    def setUpTestData(cls):
        cls.student = StudentFactory.create()

    def test_student_in_group_can_read(self):
        pass


class SchoolTest(ModelTestCase):
    """Test the School model."""

    model = tutoring.models.School
    field_tests = {
        'uai_code': {
            'unique': True,
            'primary_key': True,
            'max_length': 8,
            'verbose_name': 'code UAI',
        },
        'name': {
            'verbose_name': 'nom',
        },
        'address': {
            'verbose_name': 'adresse',
        }
    }
    # TODO implement
    model_tests = {
        'verbose_name': 'lycée',
        'ordering': ('name',),
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = tutoring.models.School.objects.create(
            uai_code=random_uai_code(),
            name='Lycée Michelin')

    def test_uai_code_help_text_indicates_format(self):
        help_text = self.model._meta.get_field('uai_code').help_text
        self.assertIsNotNone(help_text)
        self.assertIn('UAI', help_text)
        self.assertIn('ex-RNE', help_text)
        self.assertIn('7 chiffres', help_text)
        self.assertIn('une lettre', help_text)

    def test_uai_code_help_text_indicates_where_to_find_it(self):
        help_text = self.model._meta.get_field('uai_code').help_text
        self.assertIn("site du ministère de l'Éducation Nationale", help_text)

    def test_get_absolute_url(self):
        url = self.obj.get_absolute_url()
        self.assertEqual(url, f'/api/schools/{self.obj.uai_code}/')
        response = self.client.get(f'/api/schools/{self.obj.uai_code}/',
                                   follow=True)
        self.assertEqual(200, response.status_code)


class TutoringSessionTest(ModelTestCase):
    """Test the TutoringSession model."""

    model = tutoring.models.TutoringSession
    field_tests = {
        'date': {
            'verbose_name': 'date',
        },
        'start_time': {
            'verbose_name': 'heure de début',
        },
        'end_time': {
            'verbose_name': 'heure de fin',
        },
        'tutoring_group': {
            'verbose_name': 'groupe de tutorat',
        },
    }
    # TODO implement
    model_tests = {
        'verbose_name': 'séance de tutorat',
        'verbose_name_plural': 'séances de tutorat',
        'ordering': ('date',),
    }

    @classmethod
    def setUpTestData(self):
        tutoring_group = tutoring.models.TutoringGroup.objects.create()
        self.obj = tutoring.models.TutoringSession.objects.create(
            tutoring_group=tutoring_group)

    def test_get_absolute_url(self):
        url = f'/api/tutoring/sessions/{self.obj.pk}'
        response = self.client.get(url, follow=True)
        self.assertEqual(200, response.status_code)

    def test_tutoring_group_one_to_many_relationship(self):
        self.assertEqual(tutoring.models.TutoringGroup.objects.get(),
                         self.obj.tutoring_group)
        self.assertIn(self.obj,
                      tutoring.models.TutoringGroup.objects.get()
                      .tutoring_sessions.all())
