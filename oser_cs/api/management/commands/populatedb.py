"""Populate the database with fake data."""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from tests.factory import (
    UserFactory, StudentFactory, TutorFactory, TutoringGroupFactory,
    TutorTutoringGroupFactory,
)
from users.permissions import setup_groups


class Command(BaseCommand):
    help = 'Populates the database with fake data.'

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
            setup_groups()
            n_students = 10
            StudentFactory.create_batch(n_students)
            self.stdout.write(f'Created {n_students} students.')
            self.stdout.write(self.style.SUCCESS('Populated database.'))
