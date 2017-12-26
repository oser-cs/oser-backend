"""School API tests."""

from rest_framework.test import APITestCase
from rest_framework import status

from tutoring.models import TutoringGroup
from tests.utils import AuthAPITestMixin
from tests.utils import APIReadTestMixin
from tests.utils import APIPostRequestTestMixin
from tests.factory import (
    TutoringGroupFactory, UserFactory, VpTutoratTutorFactory, SchoolFactory
)


class TutoringGroupReadTest(AuthAPITestMixin, APIReadTestMixin,
                            APITestCase):
    """Test authenticated user can read tutoring groups."""

    model = TutoringGroup
    factory = TutoringGroupFactory
    list_url = '/api/tutoring/groups/'
    retrieve_url_format = '/api/tutoring/groups/{obj.pk}/'
    data_content_keys = ('id', 'url', 'name', 'tutors', 'students',
                         'tutors_count', 'students_count', 'school',)

    def get_obj(self):
        return TutoringGroupFactory.create()

    @classmethod
    def get_user(cls):
        return UserFactory.create()


class CreateTutoringGroupStandardUser(AuthAPITestMixin,
                                      APIPostRequestTestMixin,
                                      APITestCase):
    """Test a standard user cannot create a tutoring group."""

    url = '/api/tutoring/groups/'
    expected_status_code = status.HTTP_403_FORBIDDEN

    def get_obj(self):
        school = SchoolFactory.create()
        return TutoringGroupFactory.build(school=school)

    def get_post_data(self, obj):
        return {
            'name': obj.name,
            'school': obj.school.get_absolute_url(),
        }

    @classmethod
    def get_user(cls):
        return UserFactory.create()


class CreateTutoringGroupVpTutorat(CreateTutoringGroupStandardUser):
    """Test a VP Tutorat user can create a tutoring group."""

    expected_status_code = status.HTTP_201_CREATED

    @classmethod
    def get_user(cls):
        tutor = VpTutoratTutorFactory.create()
        return tutor.user
