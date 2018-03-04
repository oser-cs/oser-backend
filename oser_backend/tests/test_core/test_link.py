"""Link model tests."""

from core.models import Link
from tests.utils import ModelTestCase


class LinkTest(ModelTestCase):
    """Test the Link model."""

    model = Link
    field_tests = {
        'slug': {
            'primary_key': True,
            'unique': True,
            'null': False,
            'blank': False,
        },
        'url': {
            'verbose_name': 'URL',
        },
        'description': {},
    }
    model_tests = {
        'verbose_name': 'lien',
    }

    def setUp(self):
        self.obj = Link.objects.create(slug='example-website',
                                       url='http://example.com',
                                       description="Just an example website")

    def test_str_is_slug(self):
        self.assertEqual(str(self.obj), self.obj.slug)
