"""Tutor API tests."""
from users.serializers import TutorSerializer
from tests.factory import TutorFactory
from tests.utils.api import HyperlinkedAPITestCase
from tests.test_api.mixins import ProfileEndpointsTestMixin


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
        obj = self.factory.build()
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
