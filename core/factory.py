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


class AddressFactory(factory.DjangoModelFactory):
    """Address object factory."""

    class Meta:  # noqa
        model = models.Address

    line1 = factory.Faker('street_address', locale='fr')
    # line2: None (default)
    post_code = factory.Faker('postcode', locale='fr')
    city = factory.Faker('city', locale='fr')
    # country: None (default)
