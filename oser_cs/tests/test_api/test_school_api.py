"""School API tests."""

from rest_framework.test import APITestCase

from tutoring.models import School

from tests.factory import SchoolFactory, UserFactory
from tests.utils import AuthAPITestMixin
from tests.utils import APIReadTestMixin
from tests.utils import APIPostRequestTestMixin


class SchoolReadTest(AuthAPITestMixin, APIReadTestMixin, APITestCase):
    """Test reading schools from API as authenticated user."""

    model = School
    factory = SchoolFactory
    list_url = '/api/schools/'
    retrieve_url_format = '/api/schools/{obj.pk}/'
    data_content_keys = ('uai_code', 'students', 'name', 'url',
                         'students_count',)

    @classmethod
    def get_user(cls):
        return UserFactory.create()


class SchoolCreateTest(AuthAPITestMixin, APIPostRequestTestMixin, APITestCase):
    """Test creating a school as an authenticated user."""

    url = '/api/schools/'

    @classmethod
    def get_user(cls):
        return UserFactory.create()

    def get_obj(self):
        return SchoolFactory.build()

    def get_post_data(self, obj):
        return {
            'name': obj.name,
            'uai_code': obj.uai_code,
            'address': obj.address,
        }
