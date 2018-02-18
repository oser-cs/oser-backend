"""Article model tests."""

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from showcase_site.models import Article
from showcase_site.serializers import ArticleSerializer
from tests.factory import ArticleFactory, CategoryFactory
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
        }
    }
    model_tests = {
        'verbose_name': 'article',
        'ordering': ('-pinned', '-published',),
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


class ArticleSerializerTestCase(TestCase):

    def setUp(self):
        factory = APIRequestFactory()
        self.request = factory.get('/api/')


class TestArticleSerializer(ArticleSerializerTestCase):

    def setUp(self):
        super().setUp()
        self.obj = ArticleFactory.create()
        self.serializer = ArticleSerializer(
            instance=self.obj,
            context={'request': self.request})

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data), set([
            'id', 'url', 'title', 'slug',
            'content', 'published', 'image',
            'pinned', 'categories']))

    def test_slug_is_read_only(self):
        self.assertTrue(self.serializer.fields['slug'].read_only)


class TestArticleCategories(ArticleSerializerTestCase):
    """Test the ArticleSerializer's categories field.

    It is an instance of CategoryField and convert the article's categories
    objects to a list of their titles.
    """

    def setUp(self):
        super().setUp()
        # create an article with a few categories
        self.obj = ArticleFactory.create()
        for cat in CategoryFactory.create_batch(3):
            self.obj.categories.add(cat)
        self.obj.save()
        # create the serializer
        self.serializer = ArticleSerializer(
            instance=self.obj,
            context={'request': self.request})

    def test_contains_categories_titles(self):
        expected = set(self.serializer.data['categories'])
        actual = set(c.title for c in self.obj.categories.all())
        self.assertEqual(actual, expected)
