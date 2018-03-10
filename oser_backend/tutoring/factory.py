"""Tutoring factories."""

from datetime import timedelta
import factory
import factory.django
import pytz
from django.contrib.auth import get_user_model
from django.utils import timezone
from . import models
from tutoring.utils import random_uai_code

User = get_user_model()
utc = pytz.UTC


# Create test objects factories here

class SchoolFactory(factory.DjangoModelFactory):
    """School object factory."""

    class Meta:  # noqa
        model = models.School
        exclude = ('school_name',)

    uai_code = factory.LazyFunction(random_uai_code)
    school_name = factory.Faker('name', locale='fr')
    name = factory.LazyAttribute(lambda o: 'Lycée {o.school_name}'.format(o=o))
    address = factory.Faker('address', locale='fr')


class TutoringGroupFactory(factory.DjangoModelFactory):
    """TutoringGroup object factory."""

    class Meta:  # noqa
        model = models.TutoringGroup
        exclude = ('level',)

    level = factory.Iterator(['Seconde', 'Première', 'Terminale'])
    name = factory.LazyAttribute(
        lambda o: '{o.school} ({o.level})'.format(o=o))
    school = factory.SubFactory(SchoolFactory)


class TutorTutoringGroupFactory(factory.DjangoModelFactory):
    """Intermediate tutor-tutoring group object factory."""

    class Meta:  # noqa
        model = models.TutorTutoringGroup

    # tutor can be passed on creation
    tutoring_group = factory.SubFactory(TutoringGroupFactory)
    is_leader = False


class TutoringSessionFactory(factory.DjangoModelFactory):
    """Tutoring session object factory."""

    class Meta:  # noqa
        model = models.TutoringSession

    # random date 30 days ahead in time
    date = factory.Faker('future_date', end_date='+30d')
    start_time = factory.LazyFunction(timezone.now)
    end_time = factory.LazyAttribute(
        lambda o: o.start_time + timedelta(hours=2))
    tutoring_group = factory.SubFactory(TutoringGroupFactory)
