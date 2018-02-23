"""Populate the database with fake data."""

import random

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from tests.factory import (ArticleFactory, CategoryFactory, KeyFigureFactory,
                           StudentFactory, TestimonyFactory, VisitFactory)

from showcase_site.models import Category

from .utils import DataLoader, get_model, watcher


class Command(BaseCommand):
    """Populate the database with fake data."""

    help = 'Populate the database with fake data.'
    affected = list(
        map(
            get_model,
            (StudentFactory, CategoryFactory, ArticleFactory,
             TestimonyFactory, KeyFigureFactory,
             VisitFactory)
        ))

    def add_arguments(self, parser):
        parser.add_argument(
            '--cleanbefore',
            action='store_true',
            dest='cleanbefore',
            help='Delete all objects of affected models before populating.',
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            dest='clean',
            help='Delete all objects of affected models and exit.',
        )
        parser.add_argument(
            '--preview',
            action='store_true',
            dest='preview',
            help='Show affected models and exit.'
        )

    def create_students(self):
        StudentFactory.create_batch(5)

    def create_categories(self):
        category_titles = [
            title for title in ('Annonces', 'Sorties', 'Focus Europe')
            if not Category.objects.filter(title=title)
        ]
        if not category_titles:
            return
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
        for image in DataLoader('article-{i}.jpg', 5):
            article = ArticleFactory.create(image=image)
            self.add_random_categories(article)
            article.save()

    def create_testimonies(self):
        TestimonyFactory.create_batch(3)

    def create_key_figures(self):
        KeyFigureFactory.create_batch(4)

    def create_visits(self):
        for image in DataLoader('visit-{i}.jpg', 8):
            VisitFactory.create(image=image)

    @watcher(*affected)
    def create(self):
        self.create_students()
        self.create_categories()
        self.create_articles()
        self.create_testimonies()
        self.create_key_figures()
        self.create_visits()

    @watcher(*affected)
    def _clean(self):
        for model in self.affected:
            model.objects.all().delete()

    def clean(self):
        self._clean()
        call_command('clean_media')
        self.stdout.write(self.style.SUCCESS('Cleaned populated database.'))

    def preview(self):
        if self.affected:
            self.stdout.write(
                self.style.NOTICE('The following models will be affected:'))
        for model in self.affected:
            self.stdout.write(model._meta.label)

    def handle(self, *args, **options):
        with transaction.atomic():
            if options.get('preview'):
                self.preview()
            elif options.get('clean'):
                self.clean()
            else:
                if options.get('cleanbefore', False):
                    self.clean()
                self.create()
                self.stdout.write(self.style.SUCCESS('Populated database.'))
        self.check()
