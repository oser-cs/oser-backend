"""Showcase site factories."""

import random
import factory
import factory.django
import pytz
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()
utc = pytz.UTC


class ArticleFactory(factory.DjangoModelFactory):
    """Article object factory."""

    class Meta:  # noqa
        model = models.Article

    title = factory.Faker('sentence', locale='fr')
    content = factory.Faker('text', max_nb_chars=2000, locale='fr')
    introduction = factory.Faker('text', max_nb_chars=200, locale='fr')
    published = factory.Faker('date')
    pinned = factory.Iterator((True, False, False, False))


class CategoryFactory(factory.DjangoModelFactory):
    """Category object factory."""

    class Meta:  # noqa
        model = models.Category
        exclude = ('_title',)

    _title = factory.Faker('word')

    @factory.lazy_attribute
    def title(self):
        """Category title is subject to a unique constraint.

        Add a random number if the fake title already exists.
        """
        if models.Category.objects.filter(title=self._title).exists():
            return self._title + str(random.randint(0, 100))
        return self._title


class TestimonyFactory(factory.DjangoModelFactory):
    """Testimony object factory."""

    class Meta:  # noqa
        model = models.Testimony

    source = factory.Faker('name', locale='fr')
    quote = factory.Faker('text', max_nb_chars=200, locale='fr')


class KeyFigureFactory(factory.DjangoModelFactory):
    """Key figure object factory."""

    class Meta:  # noqa
        model = models.KeyFigure

    figure = factory.LazyFunction(lambda: random.randint(10, 200))
    description = factory.Faker('text', max_nb_chars=60, locale='fr')
    order = factory.Sequence(lambda n: n)


class PartnerFactory(factory.DjangoModelFactory):
    """Partner object factory."""

    class Meta:  # noqa
        model = models.Partner

    name = factory.Faker('company', locale='fr')
    website = factory.Faker('url')
    logo = factory.Faker('image_url', height=320)
    # 40% of partnerships will be premium on average
    premium = factory.LazyFunction(
        lambda: random.choices([True, False], weights=[.4, .6])[0])
    # 90% of partnerships will be active on average
    active = factory.LazyFunction(
        lambda: random.choices([True, False], weights=[.9, .1])[0])


class ActionFactory(factory.DjangoModelFactory):
    """Action object factory."""

    class Meta:  # noqa
        model = models.Action

    title = factory.Faker('text', max_nb_chars=30)
    description = factory.Faker('text', max_nb_chars=300)
    key_figure = factory.Faker('text', max_nb_chars=100)
    highlight = factory.LazyFunction(
        lambda: random.choices([True, False], weights=[.6, .4])[0]
    )
