"""KeyFigure model tests."""
import showcase_site.models
from showcase_site.factory import KeyFigureFactory
from tests.utils import ModelTestCase


class KeyFigureTest(ModelTestCase):
    """Test the KeyFigure model."""

    model = showcase_site.models.KeyFigure
    field_tests = {
        'figure': {
            'verbose_name': 'chiffre',
        },
        'description': {
            'max_length': 100,
        },
        'order': {
            'verbose_name': 'ordre',
            # v required by adminsortable
            'default': 0,
            'editable': True,
            # ^
        },
    }
    model_tests = {
        'verbose_name': 'chiffre clé',
        'verbose_name_plural': 'chiffres clés',
        'ordering': ('order',),
    }

    def test_description_is_saved_as_lowercase(self):
        obj = KeyFigureFactory.create(description='TO LOWERCASE')
        self.assertEqual(obj.description, 'to lowercase')
