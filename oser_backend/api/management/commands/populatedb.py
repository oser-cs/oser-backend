"""Populate the database with fake data."""

import os
import random
from itertools import cycle
from contextlib import contextmanager
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from django.core.files import File

from showcase_site.models import Category
from tests.factory import StudentFactory
from tests.factory import ArticleFactory
from tests.factory import CategoryFactory
from tests.factory import TestimonyFactory


HERE = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(HERE, 'data')


def article_filename(i):
    return 'article-{}.jpg'.format(i)


def count_article_images():
    count = 0
    while os.path.exists(os.path.join(data_path, article_filename(count))):
        count += 1
    return count


num_images = count_article_images()


def article_images(number):
    images = cycle(range(num_images))
    for _ in range(number):
        filename = article_filename(next(images))
        path = os.path.join(data_path, filename)
        with open(path, 'rb') as img:
            wrapped_img = File(img)
            # Default name of the file is the full path to img.
            # Use only the filename.
            wrapped_img.name = filename
            yield wrapped_img


def create(f):
    return f


def clean(f):
    return f


class Command(BaseCommand):
    """Populate the database with fake data."""

    help = 'Populate the database with fake data.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flushbefore',
            action='store_true',
            dest='flushbefore',
            help='Call manage.py flush before populating the database',
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            dest='clean',
            help='Remove previously generated objects from database',
        )

    @contextmanager
    def creating(self, factory_class, amount):
        """Automatically print a line with number of created objects."""
        plural = factory_class._meta.model._meta.verbose_name_plural
        try:
            yield amount
            self.stdout.write('Created {} {}.'.format(amount, plural))
        finally:
            pass

    def create_students(self):
        with self.creating(StudentFactory, 10) as n:
            StudentFactory.create_batch(n)

    def create_categories(self):
        category_titles = [
            title for title in ('Annonces', 'Sorties', 'Focus Europe')
            if not Category.objects.filter(title=title)
        ]
        if not category_titles:
            return
        with self.creating(CategoryFactory, len(category_titles)):
            for title in category_titles:
                CategoryFactory.create(title=title)

    def add_random_categories(self, article):
        ids = tuple(Category.objects.values_list('id', flat=True))
        amount = min(len(ids), random.randint(0, 3))
        rand_ids = random.sample(ids, amount)
        categories = Category.objects.filter(id__in=rand_ids)
        for category in categories:
            article.categories.add(category)
        else:
            self.stdout.write('Added {} categories to {}'
                              .format(categories.count(), article))

    def create_articles(self):
        with self.creating(ArticleFactory, 3) as n:
            for image in article_images(n):
                article = ArticleFactory.create(image=image)
                self.add_random_categories(article)
                article.save()

    def create_testimonies(self):
        with self.creating(TestimonyFactory, 6) as n:
            TestimonyFactory.create_batch(n)

    def clean(self):
        StudentFactory._meta.model.objects.all().delete()
        Category.objects.all().delete()
        ArticleFactory._meta.model.objects.all().delete()
        TestimonyFactory._meta.model.objects.all().delete()
        call_command('clean_media')
        self.stdout.write(self.style.SUCCESS('Cleaned populated database.'))

    def handle(self, *args, **options):
        with transaction.atomic():
            if options.get('flushbefore', False):
                call_command('flush')
            if options.get('clean', False):
                self.clean()
            else:
                self.create_students()
                self.create_categories()
                self.create_articles()
                self.create_testimonies()
                self.stdout.write(self.style.SUCCESS('Populated database.'))
        self.check()
