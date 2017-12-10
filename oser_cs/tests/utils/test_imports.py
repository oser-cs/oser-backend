"""Test utils imports."""

from django.test import TestCase


class UtilsImportsTest(TestCase):
    """Test utils imports work properly."""

    def test_import_meta_test_case(self):
        from tests.utils import MetaTestCase

    def test_import_field_test_case(self):
        from tests.utils import FieldTestCase

    def test_import_model_test_case(self):
        from tests.utils import ModelTestCase

    def test_import_abstract_model_test_case(self):
        from tests.utils import MixinModelTestCase

    def test_import_random_email(self):
        from tests.utils import random_email

    def test_import_random_uai_code(self):
        from tests.utils import random_uai_code
