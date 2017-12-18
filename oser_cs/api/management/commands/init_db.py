"""Initialize the database data."""

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.contrib.auth.models import Group
from users.models import User, Tutor, Student
from tutoring.models import (
    School, TutoringGroup, TutoringGroupLeadership)
from tests.utils import random_uai_code


class Command(BaseCommand):
    help = 'Initialize the database with initial data'

    def handle(self, *args, **options):
        try:
            # Create auth groups
            from tutoring.models import VP_TUTORAT_GROUP
            Group.objects.create(name=VP_TUTORAT_GROUP)

            # Create users
            florimondmanca = User.objects.create(
                email='florimond.manca@student.ecp.fr',
                first_name='Florimond',
                last_name='Manca',
                is_superuser=True,
                is_staff=True,
            )
            florimondmanca.set_password('coaster96')
            florimondmanca.save()

            johndoe = User.objects.create(
                email='john.doe@example.net',
                first_name='John',
                last_name='Doe',
                date_of_birth='1996-01-01',
            )
            johndoe.set_password('pwsecretpw')
            johndoe.save()

            sarahlink = User.objects.create(
                email='sarah.link@example.net',
                first_name='Sarah',
                last_name='Link',
                date_of_birth='2000-01-01',
            )
            sarahlink.set_password('pwsecretpw')
            sarahlink.save()
            self.stdout.write('Created 3 users')

            # Create a tutor
            tutor = Tutor.objects.create(
                user=johndoe,
                promotion=2019,
            )
            self.stdout.write('Created 1 tutor')

            # Create a student
            student = Student.objects.create(
                user=sarahlink,
                address="4 Place des Anglais, 75000 PARIS",
            )
            self.stdout.write('Created 1 student')

            self.stdout.write(self.style.SUCCESS(
                'Successfully initialized users'))

            # Create a school
            school = School.objects.create(
                uai_code=random_uai_code(),
                name='Lycée Matisse',
                address='30 Rue des Lilas, 93100 MONTREUIL',
            )
            # Link student to school
            school.students.add(student)
            self.stdout.write('Created 1 school with 1 student')

            # Create a tutoring group
            tutoring_group = TutoringGroup.objects.create(
                name='Matisse Secondes',
            )
            # Link school, student and tutor to tutoring group
            tutoring_group.school = school
            tutoring_group.students.add(student)
            TutoringGroupLeadership.objects.create(
                tutoring_group=tutoring_group,
                tutor=tutor,
                is_leader=True,
            )
            self.stdout.write('Created 1 tutoring group for 1 school '
                              'with 1 student and 1 leader tutor')

            self.stdout.write(self.style.SUCCESS(
                'Successfully initialized tutoring'))

        except IntegrityError:
            self.stdout.write(self.style.WARNING(
                'Initialization failed: data already exists'))
