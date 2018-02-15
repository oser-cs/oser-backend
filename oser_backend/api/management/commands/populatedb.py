"""Populate the database with fake data."""

from contextlib import contextmanager
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from django.core.files import File
from tests.factory import StudentFactory, ArticleFactory


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

    @contextmanager
    def creating(self, factory_class, amount):
        plural = factory_class._meta.model._meta.verbose_name_plural
        try:
            yield amount
            self.stdout.write('Created {} {}.'.format(amount, plural))
        finally:
            pass

    def handle(self, *args, **options):
        with transaction.atomic():
            if options['flushbefore']:
                call_command('flush')

            with self.creating(StudentFactory, 10) as n:
                StudentFactory.create_batch(n)

            with self.creating(ArticleFactory, 3) as n:
                for i in range(1, n + 1):
                    filename = 'article-{}.jpg'.format(i)
                    path = 'tests/media/' + filename
                    print(path)
                    with open(path, 'rb') as img:
                        wrapped_img = File(img)
                        # Default name of the file is the full path to img.
                        # Use only the filename.
                        wrapped_img.name = filename
                        ArticleFactory.create(image=wrapped_img)

            self.stdout.write(self.style.SUCCESS('Populated database.'))
        self.check()
