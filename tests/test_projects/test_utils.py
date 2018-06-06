"""Test projects utilities."""

from django.test import TestCase
from projects.utils import this_year


class ThisYearTest(TestCase):
    """Test the this_year() function."""

    def test_is_integer(self):
        self.assertIsInstance(this_year(), int)
