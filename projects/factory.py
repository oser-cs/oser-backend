"""Projects factories."""

import factory
import factory.django

from users.factory import UserFactory
from .models import Project, Edition, Participation


class ProjectFactory(factory.DjangoModelFactory):
    """Project object factory."""

    class Meta:  # noqa
        model = Project
        exclude = ('_description',)

    name = factory.Faker('company')
    _description = factory.Faker('sentences', locale='fr')
    description = factory.LazyAttribute(lambda o: '\n'.join(o._description))
    logo = factory.django.ImageField(color='green')


class EditionFactory(factory.DjangoModelFactory):
    """Edition object factory."""

    class Meta:  # noqa
        model = Edition
        exclude = ('_description',)

    _description = factory.Faker('sentences', locale='fr')
    description = factory.LazyAttribute(lambda o: '\n'.join(o._description))

    @factory.lazy_attribute
    def project(self):
        """Return an existing project or a new one if none exists."""
        project = Project.objects.first()
        return project and project or ProjectFactory.create()


class ParticipationFactory(factory.DjangoModelFactory):
    """Participation object factory."""

    class Meta:  # noqa
        model = Participation

    user = factory.SubFactory(UserFactory)

    @factory.lazy_attribute
    def edition(self):
        """Return an existing edition or a new one if none exists."""
        edition = Edition.objects.first()
        return edition and edition or EditionFactory.create()
