"""School API tests."""

from rest_framework import status

from tutoring.models import TutoringGroup

from tests.utils import AuthModelAPITestCase
from tests.factory import (
    TutoringGroupFactory, UserFactory, VpTutoratTutorFactory,
    SchoolFactory,
)


class TutoringGroupAPIAsStandardUser(AuthModelAPITestCase):
    """Test the tutoring group API for standard users."""

    model = TutoringGroup

    @classmethod
    def get_user(cls):
        return UserFactory.create()

    def test_can_list(self):
        n_items = 5
        for _ in range(n_items):
            TutoringGroupFactory.create()
        url = '/api/tutoring/groups/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), n_items)

    def test_can_retrieve(self):
        obj = TutoringGroupFactory.create()
        response = self.client.get(obj.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_has_expected_values(self):
        obj = TutoringGroupFactory.create()
        response = self.client.get(obj.get_absolute_url())
        keys = (
            'id', 'url', 'name', 'tutors', 'students',
            'tutors_count', 'students_count',
            'school',
        )
        for key in keys:
            self.assertIn(key, response.data)

    def test_cannot_create(self):
        obj = TutoringGroupFactory.create()
        data = {
            'name': obj.name,
            'school': obj.school.get_absolute_url(),
            'tutors': obj.tutors.all(),
            'students': obj.students.all(),
        }
        url = '/api/tutoring/groups/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TutoringGroupAPIAsVpTutorat(AuthModelAPITestCase):
    """Test the tutoring group API for VP Tutorat users."""

    model = TutoringGroup

    @classmethod
    def get_user(cls):
        tutor = VpTutoratTutorFactory.create()
        return tutor.user

    def test_can_create(self):
        """Ensure a VP Tutorat can create new tutoring group."""
        school = SchoolFactory.create()
        obj = TutoringGroupFactory.build(school=school)
        data = {
            'name': obj.name,
            'school': obj.school.get_absolute_url(),
            'tutors': [],
            'students': [],
        }
        url = '/api/tutoring/groups/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
