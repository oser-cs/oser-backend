"""Tutoring group API tests."""

from rest_framework import status

from tests.factory import TutoringGroupFactory, SchoolFactory
from tests.factory import UserFactory, VpTutoratTutorFactory
from tutoring.serializers import TutoringGroupSerializer
from tests.utils.api import HyperlinkedAPITestCase


class TutoringGroupEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the tutoring group endpoints."""

    factory = TutoringGroupFactory
    serializer_class = TutoringGroupSerializer

    def test_list(self):
        url = '/api/tutoring/groups/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        obj = self.factory.create()
        url = '/api/tutoring/groups/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def perform_create(self, user=None):
        if user is not None:
            self.client.force_login(user)
        url = '/api/tutoring/groups/'
        school = SchoolFactory.create()
        obj = self.factory.build(school=school, id=123)
        data = self.serialize(obj, 'post', url)
        response = self.client.post(url, data, format='json')
        return response

    def test_create_anonymous_user_forbidden(self):
        self.assertForbidden(self.perform_create, user=None)

    def test_create_regular_user_forbidden(self):
        self.assertForbidden(self.perform_create, user=UserFactory.create())

    def test_create_as_vp_tutorat_allowed(self):
        tutor = VpTutoratTutorFactory.create()
        self.assertAuthorized(self.perform_create, user=tutor.user,
                              expected_status_code=status.HTTP_201_CREATED)

    def perform_update(self):
        obj = self.factory.create()
        url = '/api/tutoring/groups/{obj.pk}/'.format(obj=obj)
        data = self.serialize(obj, 'put', url)
        data['name'] = 'Modified name'
        response = self.client.put(url, data, format='json')
        return response

    def test_update_anonymous_user_forbidden(self):
        self.assertForbidden(self.perform_update, user=None)

    def test_update_regular_user_forbidden(self):
        self.assertForbidden(self.perform_update, user=UserFactory.create())

    def test_update_vp_tutorat_allowed(self):
        tutor = VpTutoratTutorFactory.create()
        self.assertAuthorized(self.perform_update, user=tutor.user,
                              expected_status_code=status.HTTP_200_OK)

    def perform_partial_update(self):
        obj = self.factory.create()
        url = '/api/tutoring/groups/{obj.pk}/'.format(obj=obj)
        data = {'name': 'Modified name'}
        response = self.client.patch(url, data, format='json')
        return response

    def test_partial_update_anonymous_user_forbidden(self):
        self.assertForbidden(self.perform_partial_update, user=None)

    def test_partial_update_regular_user_forbidden(self):
        self.assertForbidden(self.perform_partial_update,
                             user=UserFactory.create())

    def test_partial_update_vp_tutorat_allowed(self):
        tutor = VpTutoratTutorFactory.create()
        self.assertAuthorized(self.perform_partial_update, user=tutor.user,
                              expected_status_code=status.HTTP_200_OK)

    def perform_delete(self):
        obj = self.factory.create()
        url = '/api/tutoring/groups/{obj.pk}/'.format(obj=obj)
        response = self.client.delete(url)
        return response

    def test_delete_anonymous_user_forbidden(self):
        self.assertForbidden(self.perform_delete, user=None)

    def test_delete_regular_user_forbidden(self):
        self.assertForbidden(self.perform_delete,
                             user=UserFactory.create())

    def test_delete_vp_tutorat_allowed(self):
        tutor = VpTutoratTutorFactory.create()
        self.assertAuthorized(self.perform_delete, user=tutor.user,
                              expected_status_code=status.HTTP_204_NO_CONTENT)
