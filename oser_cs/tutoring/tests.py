"""Tutoring tests."""

from django.contrib.auth import get_user_model
from tutoring.models import TutoringGroup, School
from persons.models import Tutor
from tests.utils import ModelTestCase, random_uai_code, random_email


User = get_user_model()


class TutoringGroupTest(ModelTestCase):
    """Test the TutoringGroup model."""

    model = TutoringGroup
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
    def setUpTestData(self):
        self.obj = TutoringGroup.objects.create()

    def test_get_absolute_url(self):
        response = self.client.get(f'/api/tutoringgroups/{self.obj.pk}',
                                   follow=True)
        self.assertEqual(200, response.status_code)

    def test_tutors_many_to_many_relationship(self):
        user = User.objects.create(email=random_email())
        tutor = Tutor.objects.create(user=user)
        tutor.tutoring_groups.add(self.obj)
        self.assertIn(tutor, self.obj.tutors.all())
        self.assertIn(self.obj, tutor.tutoring_groups.all())


class SchoolTest(ModelTestCase):
    """Test the School model."""

    model = School
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
    def setUpTestData(self):
        self.obj = School.objects.create(uai_code=random_uai_code())

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
        response = self.client.get(f'/api/schools/{self.obj.pk}',
                                   follow=True)
        self.assertEqual(200, response.status_code)
