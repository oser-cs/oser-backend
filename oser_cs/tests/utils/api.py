"""API test utilities."""

from rest_framework.test import APITestCase


__all__ = ('ModelAPITestCase',)


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
