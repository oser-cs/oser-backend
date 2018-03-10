"""Initialize admin users."""

from io import StringIO
from django.test import TestCase
from django.conf import settings
from django.core.management import call_command
from django.contrib.auth import get_user_model
from users.factory import UserFactory

User = get_user_model()


class InitAdminTest(TestCase):
    """Test the initadmin command."""

    out = StringIO()

    def count_created(self):
        """Count number of users created by the command."""
        before = User.objects.count()
        call_command('initadmin', verbosity=0, stdout=self.out)
        after = User.objects.count()
        return after - before

    def test_no_user_has_created_admin(self):
        self.assertEqual(self.count_created(), len(settings.ADMINS))

    def test_user_exists_has_not_created_admin(self):
        UserFactory.create()
        self.assertEqual(self.count_created(), 0)
