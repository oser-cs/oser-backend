"""Address API tests."""

from django.test import TestCase

from core.factory import AddressFactory
from core.serializers import AddressSerializer
from tests.utils import SerializerTestCaseMixin


class TestAddressSerializer(SerializerTestCaseMixin, TestCase):
    """Test the Address serializer."""

    serializer_class = AddressSerializer
    factory_class = AddressFactory

    expected_fields = (
        'line1', 'line2', 'post_code', 'city',
        {'country': ('name', 'code')},
    )
