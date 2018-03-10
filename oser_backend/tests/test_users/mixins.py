"""Users test mixins."""

from users.factory import UserFactory


class ProfileTestMixin:
    """Common tests for all profiles."""

    def test_get_absolute_url(self):
        self.client.force_login(UserFactory.create())
        url = self.obj.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
