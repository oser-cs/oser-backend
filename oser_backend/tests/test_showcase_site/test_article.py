"""Article model tests."""
from showcase_site.models import Article
from tests.factory import ArticleFactory
from tests.utils import ModelTestCase

import showcase_site.models


class ArticleTest(ModelTestCase):
    """Test the Article model."""

    model = showcase_site.models.Article
    field_tests = {
        'published': {
            'verbose_name': 'date de publication',
        },
        'title': {
            'max_length': 300,
            'verbose_name': 'titre',
        },
        'content': {
            'verbose_name': 'contenu',
        },
        'image': {
            'verbose_name': 'illustration',
        },
        'pinned': {
            'verbose_name': 'épinglé',
            'default': False,
        },
        'categories': {
            'verbose_name': 'catégories',
        }
    }
    model_tests = {
        'verbose_name': 'article',
        'ordering': ('-published',),
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = ArticleFactory.create(title='This is an article')

    def test_slug_filled_from_title(self):
        obj = Article.objects.create(title='This is another article')
        self.assertEqual(obj.slug, 'this-is-another-article')

    def test_get_absolute_url(self):
        url = self.obj.get_absolute_url()
        expected = '/api/articles/{}/'.format(self.obj.pk)
        self.assertEqual(url, expected)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
