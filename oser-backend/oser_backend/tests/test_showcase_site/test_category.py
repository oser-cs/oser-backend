"""Category model tests."""

from django.test import TestCase

import showcase_site.models
from showcase_site.factory import ArticleFactory, CategoryFactory
from showcase_site.models import Category
from showcase_site.serializers import CategoryField
from tests.utils import ModelTestCase


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


class TestCategoryField(TestCase):
    """Test the custom category relation field."""

    def setUp(self):
        self.obj = CategoryFactory.create()
        self.field = CategoryField()

    def test_representation_is_title(self):
        data = self.field.to_representation(self.obj)
        self.assertEqual(data, self.obj.title)

    def test_internal_value_builds_category_from_title(self):
        obj = self.field.to_internal_value(self.obj.title)
        self.assertEqual(obj, self.obj)

    def test_internal_value_from_unknown_title_raises_error(self):
        with self.assertRaises(Category.DoesNotExist):
            self.field.to_internal_value('unknown')
