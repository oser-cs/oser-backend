"""Users API tests."""


from django.template.defaulttags import date
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from tests.factory import UserFactory
from tests.utils import AuthAPITestMixin
from tests.utils import APIPostRequestTestMixin
from tests.utils import APIReadTestMixin


User = get_user_model()


class UserReadTest(AuthAPITestMixin, APIReadTestMixin, APITestCase):
    """Test authenticated users can read users."""

    model = User
    factory = UserFactory
    list_url = '/api/users/'
    retrieve_url_format = '/api/users/{obj.pk}/'
    data_content_keys = (
        'id', 'url', 'first_name', 'last_name', 'email', 'date_of_birth',
        'phone_number', 'gender', 'profile',
    )

    @classmethod
    def get_user(cls):
        return UserFactory.create()


class UserCreateTest(APIPostRequestTestMixin, APITestCase):
    """Test anonymous user can create a user."""

    url = '/api/users/'

    def get_obj(self):
        return UserFactory.build()

    def get_post_data(self, obj):
        return {
            'email': obj.email,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'phone_number': obj.phone_number,
            'date_of_birth': obj.date_of_birth.strftime('%d/%m/%Y'),
            'gender': obj.gender,
            'profile_type': obj.profile_type,
            'password': 'secret',
        }
