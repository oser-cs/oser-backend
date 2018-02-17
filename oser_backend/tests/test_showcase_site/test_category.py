"""Category model tests."""

from showcase_site.models import Category
from tests.utils import ModelTestCase
from tests.factory import ArticleFactory

import showcase_site.models


class CategoryTest(ModelTestCase):
    """Test the Category model."""

    model = showcase_site.models.Category
    field_tests = {
        'title': {
            'max_length': 100,
            'verbose_name': 'titre',
            'unique': True,
        },
    }
    model_tests = {
        'verbose_name': 'catégorie',
        'ordering': ('title',),
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = Category.objects.create(title='Annonces')
        # create an article with this category
        cls.article = ArticleFactory.create()
        cls.article.categories.add(cls.obj)
        cls.article.save()

    def test_str_is_title(self):
        self.assertEqual(str(self.obj), self.obj.title)

    def test_articles_many_to_many_relationship(self):
        self.assertIn(self.article, self.obj.article_set.all())
