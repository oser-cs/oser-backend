"""Core factories."""

import factory
import factory.django
from . import models


# Create test objects factories here

class LinkFactory(factory.DjangoModelFactory):
    """Link object factory."""

    class Meta:  # noqa
        model = models.Link

    slug = factory.Faker('slug')
    url = factory.Faker('url')
    description = factory.Faker('sentence', locale='fr')
