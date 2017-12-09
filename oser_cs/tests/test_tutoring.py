"""Tutoring tests."""

from tutoring.models import School
from tests.utils import ModelTestCase


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
    # TODO implement dict-based model test generation
    model_tests = {
        'ordering': ('name',),
    }

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
