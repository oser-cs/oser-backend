"""Profile factories."""

from datetime import datetime

import factory
import factory.django
from django.contrib.auth.models import Group

from core.factory import AddressFactory
from users.factory import UserFactory

from . import models


class StudentFactory(factory.django.DjangoModelFactory):
    """Student object factory."""

    class Meta:  # noqa
        model = models.Student

    user = factory.SubFactory(UserFactory)


_this_year = datetime.today().year


class TutorFactory(factory.django.DjangoModelFactory):
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
