"""Action model tests."""

from showcase_site.factory import ActionFactory
from showcase_site.models import Action
from tests.utils import ModelTestCase


class ActionTest(ModelTestCase):
    """Test the Action model."""

    model = Action
    field_tests = {
        'title': {
            'max_length': 30,
            'verbose_name': 'titre',
        },
        'description': {
        },
        'key_figure': {
            'verbose_name': 'chiffre clé',
            'default': '',
            'blank': True,
        },
        'highlight': {
            'verbose_name': 'mettre en avant',
            'default': True,
        },
        'order': {
            'verbose_name': 'ordre',
            'default': 0,
        }
    }
    model_tests = {
        'verbose_name': 'action clé',
        'verbose_name_plural': 'actions clés',
        'ordering': ('order',),
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = ActionFactory.create()

    def test_str_is_title(self):
        self.assertEqual(str(self.obj), self.obj.title)
