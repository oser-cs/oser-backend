"""API test utilities."""

from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status

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

    def assertAuthorized(self, perform_request, user, expected_status_code):
        """Assert a user is authorized to make a given request.

        Parameters
        ----------
        perform_request : function: None -> response
            Should send the request of interest and return the response object.
        user : Django User
        expected_status_code : int
            HTTP status code.
        """
        if user is not None:
            self.client.force_login(user)
        response = perform_request()
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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
