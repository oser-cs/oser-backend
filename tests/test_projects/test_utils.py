"""Test projects utilities."""

from django.test import TestCase
from projects.utils import this_year


class ThisYearTest(TestCase):
    """Test the this_year() function."""

    def test_returns_int(self):
        self.assertIsInstance(this_year(), int)
