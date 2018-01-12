"""Populate the database with fake data."""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from tests.factory import StudentFactory


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

    def handle(self, *args, **options):
        with transaction.atomic():
            if options['flushbefore']:
                call_command('flush')
            n_students = 10
            StudentFactory.create_batch(n_students)
            self.stdout.write('Created {} students.'.format(n_students))
            self.stdout.write(self.style.SUCCESS('Populated database.'))
        self.check()
