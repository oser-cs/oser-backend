"""API test mixins."""

from contextlib import contextmanager
from rest_framework import status


class SimpleReadOnlyResourceTestMixin:
    """Test mixin for simple read-only resources.

    Must be mixed in with a SimpleAPITestCase.

    Provided tests check the following:
    - the list action is not authenticated, and returns code 200
    - the retrieve action is not authenticated, and returns code 200
    """

    list_url: str
    retrieve_url_fmt: str

    # Optional kwargs passed to factory.create() in perform_retrieve()
    retrieve_kwargs = {}

    def perform_list(self):
        response = self.client.get(self.list_url)
        return response

    def test_list_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_list,
            user=None,
            expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create(**self.retrieve_kwargs)
        url = self.retrieve_url_fmt.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_retrieve,
            user=None,
            expected_status_code=status.HTTP_200_OK)


class SignalTestMixin:
    """Mixin for testing signals."""

    @contextmanager
    def assertCalled(self, signal, **kwargs):
        """Verify that a signal is called.

        Pass `sender` to check the signal's sender too.
        """
        called = {'value': None}

        def listen(sender, **kwargs):
            called['value'] = True
            called['sender'] = sender

        signal.connect(listen)
        yield called
        signal.disconnect(listen)

        self.assertTrue(called['value'])
        if 'sender' in kwargs:
            self.assertEqual(called['sender'], kwargs['sender'])
