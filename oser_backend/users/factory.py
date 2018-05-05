"""Users factories."""

import random
from datetime import datetime

import factory
import factory.django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from tutoring.factory import TutoringGroupFactory
from tutoring.models import TutoringGroup
from utils import printable_only

from . import models

User = get_user_model()


class UserFactory(factory.DjangoModelFactory):
    """User object factory."""

    class Meta:  # noqa
        model = User
        exclude = ('uid',)

    is_staff = False
    # random but realistic first_name
    first_name = factory.Faker('first_name', locale='fr')
    # random but realistic last_name
    last_name = factory.Faker('last_name', locale='fr')
    # email built after first_name and last_name
    uid = factory.Sequence(lambda n: n)

    @factory.lazy_attribute
    def email(self):
        """Generate email for user."""
        return '{}.{}-{}@example.net'.format(
            printable_only(self.first_name.lower()),
            printable_only(self.last_name.lower()),
            self.uid)

    # this is a default, override by passing `profile_type='...'` in create()
    profile_type = None
    date_of_birth = factory.Faker('date_this_century',
                                  before_today=True, after_today=False,
                                  locale='fr')
    phone_number = factory.Faker('phone_number', locale='fr')
    gender = factory.Iterator([User.MALE, User.FEMALE])

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


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
