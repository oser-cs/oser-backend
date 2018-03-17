from django.test import TestCase
from django.core.management import call_command


class PopulateDbTest(TestCase):
    """Test the populatedb command."""

    # TODO check log outputs
    # TODO test --cleanbefore option
    # TODO test --clean option

    def test_call(self):
        """Call the command to check no error occurs."""
        call_command('populatedb', verbosity=0)
