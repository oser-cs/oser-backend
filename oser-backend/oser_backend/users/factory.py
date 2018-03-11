"""Users factories."""

from string import printable

import random
import factory
import factory.django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from tutoring.factory import SchoolFactory, TutoringGroupFactory
from tutoring.models import TutoringGroup

from . import models
from .permissions import Groups

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
        # email can only contain printable characters,
        # i.e. not "ç", no "é", ...
        def printable_only(s):
            return ''.join(c for c in filter(lambda x: x in printable, s))

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


# @factory.django.mute_signals(post_save)
class ProfileFactory(factory.DjangoModelFactory):
    """Profile object factory."""

    class Meta:  # noqa
        model = models.Profile

    user = factory.SubFactory(UserFactory)


class StudentFactory(ProfileFactory):
    """Student object factory. Not assigned to a tutoring group."""

    class Meta:  # noqa
        model = models.Student

    address = factory.Faker('address', locale='fr')


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


class TutorFactory(ProfileFactory):
    """Tutor object factory."""

    class Meta:  # noqa
        model = models.Tutor

    promotion = factory.Iterator([2019, 2020, 2021])


class TutorInGroupFactory(TutorFactory):
    """Tutor object factory included in certain user groups."""

    @factory.post_generation
    def group_names(obj, created, extracted, **kwargs):
        """Add groups using the group_names=... passed at instance creation."""
        for group_name in extracted:
            group = Group.objects.get(name=group_name)
            group.user_set.add(obj.user)


class VpTutoratTutorFactory(TutorFactory):
    """VP Tutorat tutor object factory."""

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        obj = manager.create(*args, **kwargs)
        Group.objects.get(name=Groups.G_VP_TUTORAT).user_set.add(obj.user)
        return obj


class SchoolStaffMemberFactory(ProfileFactory):
    """SchoolStaffMember object factory."""

    class Meta:  # noqa
        model = models.SchoolStaffMember

    # user = factory.SubFactory(UserFactory, profile_type='schoolstaffmember')
    school = factory.SubFactory(SchoolFactory)
    role = 'directeur'
