"""Document model tests."""

from core.models import Document
from core.factory import DocumentFactory
from tests.utils import ModelTestCase


class ArticleTest(ModelTestCase):
    """Test the Article model."""

    model = Document
    field_tests = {
        'title': {
            'max_length': 300,
            'verbose_name': 'titre',
        },
        'content': {
            'verbose_name': 'contenu',
        },
        'slug': {
            'unique': True,
            'max_length': 100,
        }
    }
    model_tests = {
        'ordering': ('title',),
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = DocumentFactory.create(title='This is a document')

    def test_slug_filled_from_title(self):
        obj = Document.objects.create(title='This is another document')
        self.assertEqual(obj.slug, 'this-is-another-document')

    def test_get_absolute_url_from_slug(self):
        url = self.obj.get_absolute_url()
        expected = '/api/documents/{}/'.format(self.obj.slug)
        self.assertEqual(url, expected)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
