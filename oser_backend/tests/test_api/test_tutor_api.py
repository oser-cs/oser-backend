"""Tutor API tests."""
from rest_framework import status
from tests.factory import TutorFactory, TutorTutoringGroupFactory, UserFactory
from tests.test_api.mixins import ProfileEndpointsTestMixin
from tests.utils.api import HyperlinkedAPITestCase

from users.serializers import TutorSerializer


class TutorEndpointsTest(ProfileEndpointsTestMixin, HyperlinkedAPITestCase):
    """Test access to the tutors endpoints.

    Regular actions tests are provided by the ProfileEndpointsTestMixin.
    """

    factory = TutorFactory
    serializer_class = TutorSerializer

    def perform_list(self):
        response = self.client.get('/api/tutors/')
        return response

    def perform_retrieve(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        response = self.client.get('/api/tutors/{obj.pk}/'.format(obj=obj))
        return response

    def perform_create(self):
        url = '/api/tutors/'
        user = UserFactory.create()
        obj = self.factory.build(user=user)
        data = self.serialize(obj, 'post', url)
        response = self.client.post(url, data, format='json')
        return response

    def perform_update(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = '/api/tutors/{obj.pk}/'.format(obj=obj)
        data = self.serialize(obj, 'put', url)
        data['promotion'] = 2020
        response = self.client.put(url, data, format='json')
        return response

    def perform_partial_update(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = '/api/tutors/{obj.pk}/'.format(obj=obj)
        data = {'promotion': 2020}
        response = self.client.patch(url, data, format='json')
        return response

    def perform_delete(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = '/api/tutors/{obj.pk}/'.format(obj=obj)
        response = self.client.delete(url)
        return response

    def test_list_tutoring_groups(self):
        def perform_list_tutoring_groups():
            obj = self.factory.create()
            # add tutor to several tutoring groups
            TutorTutoringGroupFactory.create_batch(3, tutor=obj)
            url = '/api/tutors/{}/tutoringgroups/'.format(obj.pk)
            response = self.client.get(url)
            return response

        self.assertRequiresAuth(perform_list_tutoring_groups,
                                expected_status_code=status.HTTP_200_OK)
