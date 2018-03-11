"""Tutoring tests."""

from django.test import TestCase
from users.permissions import Groups
from utils import group_exists


class TutoringTest(TestCase):
    """General tests on the tutoring app."""

    def test_VP_TUTORAT_exists(self):
        self.assertTrue(group_exists(Groups.G_VP_TUTORAT))
