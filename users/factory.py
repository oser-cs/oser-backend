"""Users factories."""

import factory
import factory.django
from django.contrib.auth import get_user_model

from utils import printable_only

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory, is_staff = False):
    """User object factory."""

    class Meta:  # noqa
        model = User
        exclude = ('uid',)

    is_staff = is_staff
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

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)
