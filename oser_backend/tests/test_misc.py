"""Various tests that don't fit in other test packages."""

from django.test import TestCase


class TestLoadSettings(TestCase):
    """Test that settings can be loaded correctly."""

    def test_load_production_settings(self):
        from oser_backend.settings.production import *

    def test_load_dev_settings(self):
        from oser_backend.settings.dev import *

    def test_load_aws_conf(self):
        from aws.conf import *
