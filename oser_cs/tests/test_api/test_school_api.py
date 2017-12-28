"""School API tests."""

from rest_framework import status
from tests.factory import SchoolFactory, VpTutoratTutorFactory
from tests.utils.api import HyperlinkedAPITestCase

from tutoring.serializers import SchoolSerializer


class SchoolEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the school endpoints."""

    factory = SchoolFactory
    serializer_class = SchoolSerializer

    def perform_list(self):
        url = '/api/schools/'
        response = self.client.get(url)
        return response

    def test_list_requires_to_be_authenticated(self):
        self.assertRequiresAuth(self.perform_list,
                                expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        url = '/api/schools/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_requires_to_be_authenticated(self):
        self.assertRequiresAuth(self.perform_retrieve,
                                expected_status_code=status.HTTP_200_OK)

    def perform_create(self):
        url = '/api/schools/'
        obj = self.factory.build()
        data = self.serialize(obj, 'post', url)
        response = self.client.post(url, data, format='json')
        return response

    def test_create_requires_more_than_authentication(self):
        self.assertAuthForbidden(self.perform_create)

    def test_create_as_vp_tutorat_allowed(self):
        tutor = VpTutoratTutorFactory.create()
        user = tutor.user
        self.assertRequestResponse(
            self.perform_create, user=user,
            expected_status_code=status.HTTP_201_CREATED)

    def perform_update(self):
        obj = self.factory.create()
        url = '/api/schools/{obj.pk}/'.format(obj=obj)
        data = self.serialize(obj, 'put', url)
        data['name'] = 'Modified name'
        response = self.client.put(url, data, format='json')
        return response

    def test_update_requires_more_than_authentication(self):
        self.assertAuthForbidden(self.perform_update)

    def test_update_as_vp_tutorat_allowed(self):
        tutor = VpTutoratTutorFactory.create()
        user = tutor.user
        self.assertRequestResponse(self.perform_update, user=user,
                                   expected_status_code=status.HTTP_200_OK)

    def perform_partial_update(self):
        obj = self.factory.create()
        url = '/api/schools/{obj.pk}/'.format(obj=obj)
        data = {'name': 'Modified name'}
        response = self.client.patch(url, data, format='json')
        return response

    def test_partial_update_requires_more_than_authentication(self):
        self.assertAuthForbidden(self.perform_partial_update)

    def test_partial_update_as_vp_tutorat_allowed(self):
        tutor = VpTutoratTutorFactory.create()
        user = tutor.user
        self.assertRequestResponse(self.perform_partial_update, user=user,
                                   expected_status_code=status.HTTP_200_OK)

    def perform_delete(self):
        obj = self.factory.create()
        url = '/api/schools/{obj.pk}/'.format(obj=obj)
        response = self.client.delete(url)
        return response

    def test_delete_requires_more_than_authentication(self):
        self.assertAuthForbidden(self.perform_delete)

    def test_delete_as_vp_tutorat_allowed(self):
        tutor = VpTutoratTutorFactory.create()
        user = tutor.user
        self.assertRequestResponse(
            self.perform_delete, user=user,
            expected_status_code=status.HTTP_204_NO_CONTENT)

    def test_list_students(self):
        pass  # TODO

    def test_list_tutors(self):
        pass  # TODO

    def test_list_staff(self):
        pass  # TODO

    def test_list_tutoring_groups(self):
        pass  # TODO

    def test_list_meetings(self):
        pass  # TODO

    def test_list_past_meetings(self):
        pass  # TODO

    def test_list_next_meetings(self):
        pass  # TODO
