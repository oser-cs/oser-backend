"""Test decorators."""

from users.factory import UserFactory


def logged_in(test_method):
    """Execute a test method with an authenticated user logged in."""
    def decorated(self, *args, **kwargs):
        self.client.force_login(UserFactory.create())
        return test_method(self, *args, **kwargs)
    return decorated
