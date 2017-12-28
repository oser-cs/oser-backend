"""API test utilities."""

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from tests.factory import UserFactory

__all__ = ('HyperlinkedAPITestCase',)


class HyperlinkedAPITestCase(APITestCase):
    """API test case suited for hyperlinked serializers."""

    serializer_class = None

    def serialize(self, obj, method, url,
                  serializer_class=None):
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
        self.assertEqual(response.status_code, expected_status_code)

    def assertForbidden(self, perform_request, user):
        """Assert a user is not authorized to make a given request.

        Parameters
        ----------
        perform_request : function: None -> response
            Should send the request of interest and return the response object.
        user : Django User
        """
        if user is not None:
            self.client.force_login(user)
        response = perform_request()
        self._check_response(perform_request, response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def assertRequiresAuth(self, perform_request, expected_status_code,
                           forbidden=False):
        """Assert a request requires to be authenticated.

        Parameters
        ----------
        perform_request : function: None -> response
            Should send the request of interest and return the response object.
        user : Django User
        expected_status_code : int
            HTTP status code.
        """
        self.assertForbidden(perform_request, user=None)
        self.assertRequestResponse(perform_request, user=UserFactory.create(),
                                   expected_status_code=expected_status_code)

    def assertAuthForbidden(self, perform_request):
        """Assert request is forbidden to anonymous and authenticated users.

        Parameters
        ----------
        perform_request : function: None -> response
            Should send the request of interest and return the response object.
        """
        self.assertForbidden(perform_request, user=None)
        self.assertForbidden(perform_request, user=UserFactory.create())
