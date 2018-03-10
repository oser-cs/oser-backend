"""School model tests."""

from django.contrib.auth import get_user_model
from tutoring.factory import SchoolFactory
from users.factory import UserFactory
from tests.utils import ModelTestCase

import tutoring.models

User = get_user_model()


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
    model_tests = {
        'verbose_name': 'lycée',
        'ordering': ('name',),
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = SchoolFactory.create(name='Lycée Michelin')

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
        self.client.force_login(UserFactory.create())
        url = self.obj.get_absolute_url()
        expected = '/api/schools/{}/'.format(self.obj.uai_code)
        self.assertEqual(url, expected)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
