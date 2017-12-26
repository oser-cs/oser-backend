"""Tutor API tests."""

from rest_framework.test import APITestCase

from users.models import Tutor
from tests.utils import AuthAPITestMixin
from tests.utils import APIReadTestMixin
from tests.utils import APIPostRequestTestMixin
from tests.factory import TutorFactory, UserFactory


class TutorReadTest(AuthAPITestMixin, APIReadTestMixin,
                    APITestCase):
    """Test read tutors from API as authenticated user."""

    model = Tutor
    factory = TutorFactory
    list_url = '/api/tutors/'
    retrieve_url = '/api/tutors/{obj.pk}/'
    data_content_keys = ('user_id', 'user', 'promotion', 'tutoring_groups',
                         'url',)

    @classmethod
    def get_user(cls):
        return UserFactory.create()


class TutorCreateTest(APIPostRequestTestMixin, APITestCase):
    """Test create tutor as anonymous user."""

    url = '/api/tutors/'

    def get_obj(self):
        user = UserFactory.create()
        obj = TutorFactory.build(user=user)
        return obj

    def get_post_data(self, obj):
        return {
            'user': obj.user.get_absolute_url(),
            'promotion': obj.promotion,
        }
