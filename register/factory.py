"""Register factories."""

import factory
import factory.django

from utils import printable_only

from . import models


class RegistrationFactory(factory.DjangoModelFactory):
    """Registration object factory."""

    class Meta:  # noqa
        model = models.Registration

    first_name = factory.Faker('first_name', locale='fr')
    last_name = factory.Faker('last_name', locale='fr')

    @factory.lazy_attribute
    def email(self):
        """Generate email for registration."""
        return '{}.{}@example.net'.format(
            printable_only(self.first_name.lower()),
            printable_only(self.last_name.lower()))
