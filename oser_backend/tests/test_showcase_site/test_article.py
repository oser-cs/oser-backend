"""Article model tests."""

from time import sleep
from django.test import TestCase
from showcase_site.models import Article, Category
from showcase_site.factory import ArticleFactory, CategoryFactory
from tests.utils import ModelTestCase

import showcase_site.models


class ArticleTest(ModelTestCase):
    """Test the Article model."""

    model = showcase_site.models.Article
    field_tests = {
        'published': {
            'verbose_name': 'publié le',
        },
        'modified': {
            'verbose_name': 'modifié le',
            'auto_now': True,
        },
        'display_image': {
            'verbose_name': "afficher l'illustration",
            'default': True,
            'blank': True,
        },
        'title': {
            'max_length': 300,
            'verbose_name': 'titre',
        },
        'content': {
            'verbose_name': 'contenu',
        },
        'introduction': {
            'blank': True,
            'default': '',
        },
        'image': {
            'verbose_name': 'illustration',
        },
        'pinned': {
            'verbose_name': 'épinglé',
            'default': False,
            'blank': True,
        },
        'categories': {
            'verbose_name': 'catégories',
        },
        'active': {
            'verbose_name': 'actif',
            'default': True,
            'blank': True,
        }
    }
    model_tests = {
        'verbose_name': 'article',
        'ordering': ('-active', '-pinned', '-published',),
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = ArticleFactory.create(title='This is an article')

    def test_slug_filled_from_title(self):
        obj = Article.objects.create(title='This is another article')
        self.assertEqual(obj.slug, 'this-is-another-article')

    def test_get_absolute_url(self):
        url = self.obj.get_absolute_url()
        expected = '/api/articles/{}/'.format(self.obj.slug)
        self.assertEqual(url, expected)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_multiple_does_not_raise_integrity_error(self):
        """Regression test.

        A previous way of assigning the slug could cause an integrity error
        because the article was always saved with slug='', but slug must
        be unique.
        """
        ArticleFactory.create(title='first article')
        ArticleFactory.create(title='second article')

    def test_was_modified(self):
        self.assertFalse(self.obj.was_modified)
        sleep(1)
        self.obj.save()
        self.assertTrue(self.obj.was_modified)


class CleanCategoriesTest(TestCase):
    """Test the clean_categories pre_delete signal on Article."""

    def setUp(self):
        # create 2 categories of articles
        self.cats = CategoryFactory.create(title='cats')
        self.dogs = CategoryFactory.create(title='dogs')
        # create an animals article that is about cats and dogs
        self.animals_article = ArticleFactory.create(title='Animals Life')
        self.animals_article.categories.add(self.cats, self.dogs)
        # create a dogs article that is only about dogs
        self.dogs_article = ArticleFactory.create(title='Dogs Life')
        self.dogs_article.categories.add(self.dogs)
        # => the cats category is only tied to the animals article.

    def exists(self, category: str):
        return Category.objects.filter(title=category).exists()

    def test_delete_animals_deletes_the_cats_category(self):
        self.assertTrue(self.exists('cats'))
        self.animals_article.delete()
        # clean_categories was triggered on 'cats' and 'dogs'.
        # cats must have been deleted because it was only tied to the
        # animals article, which has been deleted.
        self.assertFalse(self.exists('cats'))

    def test_delete_dogs_does_not_delete_cats(self):
        self.assertTrue(self.exists('cats'))
        self.dogs_article.delete()
        # clean_categories was only triggered on 'dogs'.
        # which means the cats category must still exist.
        self.assertTrue(self.exists('cats'))
