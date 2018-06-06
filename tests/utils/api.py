"""API test utilities."""

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from users.factory import UserFactory

__all__ = (
    'SimpleAPITestCase',
    'HyperlinkedAPITestCase',
    'SerializerTestCaseMixin'
)


class SimpleAPITestCase(APITestCase):
    """API test case that provides handy extra assert functions."""

    @staticmethod
    def _check_response(perform_request, response):
        if response is None:
            raise AssertionError('{} did not return a response'
                                 .format(perform_request.__name__))

    def assertRequestResponse(self, perform_request, user,
                              expected_status_code):
        """Perform a request and check the response's status code.

        Parameters
        ----------
        perform_request : function: None -> response
            Should send the request of interest and return the response object.
        user : Django User or None
            If not None, will be logged in the test client.
        expected_status_code : int
            HTTP status code.
        """
        if user is not None:
            self.client.force_login(user)
        response = perform_request()
        self._check_response(perform_request, response)
        debug = getattr(response, 'data', response)
        self.assertEqual(response.status_code, expected_status_code, debug)

    def assertUserRequestResponse(self, perform_request,
                                  expected_status_code):
        """Perform a request with an authenticated user & check status code.

        Parameters
        ----------
        perform_request : function: None -> response
            Should send the request of interest and return the response object.
        expected_status_code : int
            HTTP status code.
        """
        self.assertRequestResponse(
            perform_request,
            user=UserFactory.create(),
            expected_status_code=expected_status_code)

    def assertRequiresAuth(self, perform_request, expected_status_code=None):
        """Assert a request requires to be authenticated.

        Parameters
        ----------
        perform_request : function: None -> response
            Should send the request of interest and return the response object.
        expected_status_code : int, optional
            HTTP status code. If given, the request will be sent again
            after authenticating with a fake user, and the
            response status code will be checked against this value.
        """
        self.assertRequestResponse(
            perform_request, user=None,
            expected_status_code=status.HTTP_401_UNAUTHORIZED)
        if expected_status_code:
            self.assertUserRequestResponse(perform_request,
                                           expected_status_code)

    def assertAuthForbidden(self, perform_request):
        """Assert request is forbidden to anonymous and authenticated users.

        Parameters
        ----------
        perform_request : function: None -> response
            Should send the request of interest and return the response object.
        """
        self.assertRequiresAuth(perform_request)
        self.assertRequestResponse(
            perform_request, user=UserFactory.create(),
            expected_status_code=status.HTTP_403_FORBIDDEN)


class HyperlinkedAPITestCase(SimpleAPITestCase):
    """API test case suited for hyperlinked serializers."""

    serializer_class = None

    def serialize(self, obj, method, url, serializer_class=None):
        """Serialize an object.

        Parameters
        ----------
        obj : instance of django.db.models.Model
        method : str
            An HTTP method (case insensitive), e.g. 'post'.
        url : str
        serializer_class : subclass of rest_framework.Serializer, optional
            If not given, the test case class' serializer_class attribute
            will be used.
        """
        if serializer_class is None:
            serializer_class = self.get_serializer_class()
        request_factory = getattr(APIRequestFactory(), method.lower())
        request = request_factory(url, format='json')
        serializer = serializer_class(
            obj, context={'request': request})
        data = serializer.data
        return data

    def get_serializer_class(self):
        """Return the serializer class."""
        if self.serializer_class is None:
            raise AttributeError('serializer_class attribute not defined'
                                 'for {}'.format(self.__class__))
        return self.serializer_class


class SerializerTestCaseMixin:
    """Base test case for serializers."""

    serializer_class = None
    factory_class = None
    request_url = '/api/'
    expected_fields = ()

    def setUp(self):
        factory = APIRequestFactory()
        self.request = factory.get(self.request_url)
        self.obj = self.get_object()
        self.serializer = self.get_serializer(self.obj)

    def get_object(self):
        if self.factory_class:
            return self.factory_class.create()
        else:
            raise ValueError(
                'If factory_class is not specified, you must '
                'override get_object()')

    def get_serializer(self, obj, request=None):
        if request is None:
            request = self.request
        return self.serializer_class(instance=obj,
                                     context={'request': request})

    def test_contains_expected_fields(self):
        data = self.serializer.data

        # test nested fields passed as {'<name>': (<f1>, <f2>, ...)}
        for field in self.expected_fields:
            if isinstance(field, dict):
                name, fields = list(field.items())[0]
                data_fields = data.pop(name)
                self.assertEqual(set(data_fields), set(fields))

        # test non-nested fields
        not_nested = (field for field in self.expected_fields
                      if not isinstance(field, dict))
        self.assertEqual(set(data), set(not_nested))
