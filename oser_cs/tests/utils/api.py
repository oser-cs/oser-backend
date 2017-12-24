"""API test utilities."""

from rest_framework.test import APITestCase
from tests.factory import UserFactory

__all__ = ('ModelAPITestCase', 'AuthModelAPITestCase')


class ModelAPITestCase(APITestCase):
    """Generic model API test case."""

    model = None

    @property
    def model_name(self):
        return self.model._meta.model_name

    @property
    def model_name_plural(self):
        return self.model_name + 's'

    def create_data(self):
        return {}

    def create_obj(self, **kwargs):
        create_data = self.create_data()
        kwargs.update(create_data)
        return self.model.objects.create(**kwargs)


class AuthModelAPITestCase(ModelAPITestCase):
    """Generic model API test case with an authenticated user."""

    @classmethod
    def get_user(cls):
        """Return a user to log into the API with."""
        return UserFactory.create()

    @classmethod
    def setUpTestData(cls):
        cls.user = cls.get_user()

    def setUp(self):
        self.client.force_login(self.user)
