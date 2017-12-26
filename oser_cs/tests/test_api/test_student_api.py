"""Student API tests."""

from rest_framework.test import APITestCase

from users.models import Student
from tests.factory import (
    StudentFactory, UserFactory, SchoolFactory, TutoringGroupFactory)
from tests.utils import AuthAPITestMixin
from tests.utils import APIReadTestMixin
from tests.utils import APIPostRequestTestMixin


class StudentReadTest(AuthAPITestMixin, APIReadTestMixin, APITestCase):
    """Test read students as authenticated user."""

    model = Student
    factory = StudentFactory
    list_url = '/api/students/'
    retrieve_url_format = '/api/students/{obj.pk}/'
    data_content_keys = ('user_id', 'user', 'address', 'tutoring_group',
                         'school', 'url')

    @classmethod
    def get_user(cls):
        return UserFactory.create()


class StudentCreateTest(APIPostRequestTestMixin, APITestCase):
    """Test create student as anonymous user."""

    url = '/api/students/'

    def get_obj(self):
        user = UserFactory.create()
        school = SchoolFactory.create()
        tutoring_group = TutoringGroupFactory.create(school=school)
        obj = StudentFactory.build(user=user, school=school,
                                   tutoring_group=tutoring_group)
        return obj

    def get_post_data(self, obj):
        return {
            'user': obj.user.get_absolute_url(),
            'address': obj.address,
            'school': obj.school.get_absolute_url(),
            'tutoring_group': obj.tutoring_group.get_absolute_url(),
        }
