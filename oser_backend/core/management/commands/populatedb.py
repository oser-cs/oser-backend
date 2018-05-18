"""Populate the database with fake data."""

import random

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

import users.models
import profiles.models
import visits.models
from profiles.factory import StudentFactory, TutorFactory, TutorInGroupFactory
from visits.factory import PlaceFactory, VisitFactory

from .utils import DataLoader, SeqDataLoader, get_model, watcher


class Command(BaseCommand):
    """Populate the database with fake data."""

    help = 'Populate the database with fake data.'
    affected = list(
        map(
            get_model,
            (
                StudentFactory, TutorFactory,
                VisitFactory, PlaceFactory,
            )
        ))

    known_student_data = {
        'user__first_name': 'Jean',
        'user__last_name': 'Durant',
        'user__email': 'jean.durant@example.com',
        'user__password': 'test1234',
    }
    known_tutor_data = {
        'user__first_name': 'Martin',
        'user__last_name': 'Bond',
        'user__email': 'martin.bond@example.com',
        'user__password': 'test1234',
    }

    @property
    def known_student(self):
        return profiles.models.Student.objects.filter(
            user__email=self.known_student_data['user__email']).first()

    @property
    def known_tutor(self):
        return profiles.models.Tutor.objects.filter(
            user__email=self.known_tutor_data['user__email']).first()

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
        # create a known student
        if not self.known_student:
            StudentFactory.create(**self.known_student_data)

    def create_tutors(self):
        TutorFactory.create_batch(5)
        # create a known tutor
        if not self.known_tutor:
            TutorInGroupFactory.create(**self.known_tutor_data)

    def create_visits(self):
        with DataLoader().load('visit-factsheet.pdf') as fact_sheet:
            for image in SeqDataLoader('visit-{i}.jpg', 8):
                VisitFactory.create(image=image, fact_sheet=fact_sheet)

    def add_visit_organizers(self):
        tutors = profiles.models.Tutor.objects.all()

        def add_to_organizers(visit, user):
            visit.organizers_group.user_set.add(user)

        for visit in visits.models.Visit.objects.all():
            # add 2 organizers to each visit
            for tutor in random.choices(tutors, k=2):
                add_to_organizers(visit, tutor.user)
        # add known tutor to organizers of a visit.
        # use last visit so to be sure it will have open registrations.
        visit = visits.models.Visit.objects.last()
        if visit.organizers_group not in self.known_tutor.user.groups.all():
            add_to_organizers(visit, self.known_tutor.user)

    @watcher(*affected)
    def create(self):
        self.create_students()
        self.create_tutors()
        self.create_visits()
        self.add_visit_organizers()

    @watcher(*affected)
    def _clean(self):
        for model in self.affected:
            model.objects.all().delete()
        users.models.User.objects.filter(is_superuser=False).delete()

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
