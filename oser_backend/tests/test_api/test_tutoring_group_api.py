"""Tutoring group API tests."""

from rest_framework import status
from tutoring.factory import SchoolFactory, TutoringGroupFactory
from users.factory import VpTutoratTutorFactory
from tests.utils.api import HyperlinkedAPITestCase

from tutoring.serializers import TutoringGroupSerializer


class TutoringGroupEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the tutoring group endpoints."""

    factory = TutoringGroupFactory
    serializer_class = TutoringGroupSerializer

    def perform_list(self):
        url = '/api/tutoring/groups/'
        response = self.client.get(url)
        return response

    def test_list_requires_authentication(self):
        self.assertRequiresAuth(self.perform_list,
                                expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        url = '/api/tutoring/groups/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_requires_authentication(self):
        self.assertRequiresAuth(self.perform_retrieve,
                                expected_status_code=status.HTTP_200_OK)

    def perform_create(self, user=None):
        if user is not None:
            self.client.force_login(user)
        url = '/api/tutoring/groups/'
        school = SchoolFactory.create()
        obj = self.factory.build(school=school, id=123)
        data = self.serialize(obj, 'post', url)
        response = self.client.post(url, data, format='json')
        return response

    def test_create_requires_more_than_authentication(self):
        self.assertAuthForbidden(self.perform_create)

    def test_create_as_vp_tutorat_allowed(self):
        tutor = VpTutoratTutorFactory.create()
        self.assertRequestResponse(
            self.perform_create, user=tutor.user,
            expected_status_code=status.HTTP_201_CREATED)

    def perform_update(self):
        obj = self.factory.create()
        url = '/api/tutoring/groups/{obj.pk}/'.format(obj=obj)
        data = self.serialize(obj, 'put', url)
        data['name'] = 'Modified name'
        response = self.client.put(url, data, format='json')
        return response

    def test_update_requires_more_than_authentication(self):
        self.assertAuthForbidden(self.perform_update)

    def test_update_vp_tutorat_allowed(self):
        tutor = VpTutoratTutorFactory.create()
        self.assertRequestResponse(self.perform_update, user=tutor.user,
                                   expected_status_code=status.HTTP_200_OK)

    def perform_partial_update(self):
        obj = self.factory.create()
        url = '/api/tutoring/groups/{obj.pk}/'.format(obj=obj)
        data = {'name': 'Modified name'}
        response = self.client.patch(url, data, format='json')
        return response

    def test_partial_update_requires_more_than_authentication(self):
        self.assertAuthForbidden(self.perform_partial_update)

    def test_partial_update_vp_tutorat_allowed(self):
        tutor = VpTutoratTutorFactory.create()
        self.assertRequestResponse(
            self.perform_partial_update, user=tutor.user,
            expected_status_code=status.HTTP_200_OK)

    def perform_delete(self):
        obj = self.factory.create()
        url = '/api/tutoring/groups/{obj.pk}/'.format(obj=obj)
        response = self.client.delete(url)
        return response

    def test_delete_requires_more_than_authentication(self):
        self.assertAuthForbidden(self.perform_delete)

    def test_delete_vp_tutorat_allowed(self):
        tutor = VpTutoratTutorFactory.create()
        self.assertRequestResponse(
            self.perform_delete, user=tutor.user,
            expected_status_code=status.HTTP_204_NO_CONTENT)

    def test_list_students(self):
        pass  # TODO

    def test_add_student(self):
        pass  # TODO

    def test_remove_student(self):
        pass  # TODO

    def test_list_tutors(self):
        pass  # TODO

    def test_add_tutor(self):
        pass  # TODO

    def test_remove_tutor(self):
        pass  # TODO

    def test_list_meetings(self):
        pass  # TODO

    def test_list_past_meetings(self):
        pass  # TODO

    def test_list_next_meetings(self):
        pass  # TODO

    def test_add_meeting(self):
        pass  # TODO

    def test_remove_meeting(self):
        pass  # TODO
