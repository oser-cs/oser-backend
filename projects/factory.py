"""Projects factories."""

import factory
import factory.django

from . import models


class ProjectFactory(factory.DjangoModelFactory):
    """Project object factory."""

    class Meta:  # noqa
        model = models.Project
        exclude = ('_description',)

    name = factory.Faker('company')
    _description = factory.Faker('sentences', locale='fr')
    description = factory.LazyAttribute(lambda o: '\n'.join(o._description))
    logo = factory.django.ImageField(color='green')


class EditionFactory(factory.DjangoModelFactory):
    """Edition object factory."""

    class Meta:  # noqa
        model = models.Edition
        exclude = ('_description',)

    _description = factory.Faker('sentences', locale='fr')
    description = factory.LazyAttribute(lambda o: '\n'.join(o._description))
