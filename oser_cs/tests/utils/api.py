"""API test utilities."""

from rest_framework.test import APITestCase
from rest_framework import status


__all__ = ('ModelAPITestCase', 'AuthAPITestMixin', 'APIReadTestMixin',
           'APIPostRequestTestMixin')


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


class AuthAPITestMixin:
    """Mixin class to use a test case with a logged in user."""

    @classmethod
    def get_user(cls):
        """Return a user to log into the API with."""
        raise NotImplementedError

    @classmethod
    def setUpTestData(cls):
        cls.user = cls.get_user()

    def setUp(self):
        self.client.force_login(self.user)


class APIReadTestMixin:
    """Test mixin suited for testing read actions (list, retrieve) on models.

    Attributes
    ----------
    model : django.db.models.Model
    factory : factory.Factory
        A FactoryBoy factory used to create a test object.
    list_url : str
    retrieve_url_format : str
        Formatted string with an {obj} tag.
        Example: 'api/students/{obj.pk}/'
    n_items : int, optional
        Number of items to generate in test_list().
    data_content_keys : tuple
    """

    model = None
    factory = None
    list_url = ''
    retrieve_url_format = ''
    n_items = 5
    data_content_keys = ()

    def test_list(self):
        """Test the list action.

        Creates a list of objects and performs an HTTP GET at `list_url`.
        Succeeds if request status code is 200.
        """
        n_before = self.model.objects.all().count()
        self.factory.create_batch(self.n_items)
        url = self.list_url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data) - n_before, self.n_items)

    def test_retrieve(self):
        """Test the retrieve action.

        Retrieves an object as in test_retrieve and checks that keys specified
        in `data_content_keys` are contained in response.data.
        """
        obj = self.factory.create()
        url = self.retrieve_url_format.format(obj=obj)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_content(self):
        """Test the content of a retrieve action data.

        Retrieves an object as in test_retrieve and checks that keys specified
        in `data_content_keys` are contained in response.data.
        """
        obj = self.factory.create()
        url = obj.get_absolute_url()
        response = self.client.get(url)
        keys = self.data_content_keys
        for key in keys:
            self.assertIn(key, response.data)


class APIRequestTestMixin:
    """Generic API request test mixin."""

    url = ''
    expected_status_code = None

    def get_url(self):
        return self.url


class APIPostRequestTestMixin(APIRequestTestMixin):
    """Generic API POST request test mixin."""

    expected_status_code = status.HTTP_201_CREATED

    def get_obj(self):
        """Return a test object to extract POST data from."""
        raise NotImplementedError

    def get_post_data(self, obj):
        """Return data to send in POST request."""
        raise NotImplementedError

    def test_post(self):
        """Perform the POST request test."""
        obj = self.get_obj()
        data = self.get_post_data(obj)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, self.expected_status_code)
