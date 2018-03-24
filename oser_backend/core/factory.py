"""Core factories."""

import factory
import factory.django
from . import models


class DocumentFactory(factory.DjangoModelFactory):
    """Document object factory."""

    class Meta:  # noqa
        model = models.Document

    title = factory.Faker('sentence', locale='fr')
    content = factory.Faker('text', max_nb_chars=1000, locale='fr')
