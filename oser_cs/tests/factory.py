"""Define test objects factories.

FactoryBoy docs: http://factoryboy.readthedocs.io/en/latest/index.html
"""

import factory
import factory.django
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
import users.models
import tutoring.models
from tests.utils.misc import random_uai_code

User = get_user_model()


# Create test objects factories here

class UserFactory(factory.DjangoModelFactory):
    """User object factory.

    Usage
    -----
    user = UserFactory()
    user.first_name  # 'John'
    user.last_name  # 'Doe'
    user.email  # 'john.doe@example.net'
    user.date_of_birth  # '2011-04-01'
    user.phone_number  # '05 00 05 40 61'
    user.profile  # '<Student object...>'
    """

    class Meta:  # noqa
        model = User

    # random but realistic first_name
    first_name = factory.Faker('first_name')
    # random but realistic last_name
    last_name = factory.Faker('last_name')
    # email built after first_name and last_name
    email = factory.LazyAttribute(lambda o: '{}.{}@example.net'
                                  .format(o.first_name.lower(),
                                          o.last_name.lower()))
    # this is a default, override by passing `profile_type='...'` in create()
    profile_type = 'student'
    date_of_birth = factory.Faker('date_this_century',
                                  before_today=True, after_today=False,
                                  locale='fr_FR')
    phone_number = factory.Faker('phone_number', locale='fr_FR')


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.DjangoModelFactory):
    """Profile object factory."""

    class Meta:  # noqa
        model = users.models.Profile

    user = factory.SubFactory(UserFactory)


class StudentFactory(ProfileFactory):
    """Student object factory."""

    class Meta:  # noqa
        model = users.models.Student

    address = factory.Faker('address', locale='fr_FR')


class TutorFactory(ProfileFactory):
    """Tutor object factory."""

    class Meta:  # noqa
        model = users.models.Tutor

    promotion = 2019


class SchoolFactory(factory.DjangoModelFactory):
    """School object factory."""

    class Meta:  # noqa
        model = tutoring.models.School

    uai_code = factory.LazyFunction(random_uai_code)
    name = factory.Faker('name', locale='fr_FR')
    address = factory.Faker('address', locale='fr_FR')


class SchoolStaffMemberFactory(ProfileFactory):
    """SchoolStaffMember object factory."""

    class Meta:  # noqa
        model = users.models.SchoolStaffMember

    school = factory.SubFactory(SchoolFactory)
    role = 'directeur'
