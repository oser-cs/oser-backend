"""Profile factories."""

import random
from datetime import datetime

import factory
import factory.django
from django.contrib.auth.models import Group

from tutoring.factory import TutoringGroupFactory
from tutoring.models import TutoringGroup
from core.factory import AddressFactory
from users.factory import UserFactory

from . import models


class StudentFactory(factory.DjangoModelFactory):
    """Student object factory. Not assigned to a tutoring group."""

    class Meta:  # noqa
        model = models.Student

    user = factory.SubFactory(UserFactory)


class StudentInTutoringGroupFactory(StudentFactory):
    """Student object factory, member of a tutoring group."""

    @factory.lazy_attribute
    def tutoring_group(self):
        """Return an existing tutoring group in 70% of cases."""
        groups = TutoringGroup.objects.all()
        if groups and random.random() > .3:
            return random.choice(groups)
        return TutoringGroupFactory.create()

    # student's school is the same as the student's tutoring group's
    school = factory.SelfAttribute('tutoring_group.school')


_this_year = datetime.today().year


class TutorFactory(factory.DjangoModelFactory):
    """Tutor object factory."""

    class Meta:  # noqa
        model = models.Tutor

    user = factory.SubFactory(UserFactory)
    promotion = factory.Iterator([_this_year, _this_year + 1, _this_year + 2])
    address = factory.SubFactory(AddressFactory)


class TutorInGroupFactory(TutorFactory):
    """Tutor object factory included in certain user groups."""

    @factory.post_generation
    def group_names(obj, created, extracted, **kwargs):
        """Add groups using the group_names=... passed at instance creation."""
        if not extracted:
            return
        for group_name in extracted:
            group = Group.objects.get(name=group_name)
            group.user_set.add(obj.user)
