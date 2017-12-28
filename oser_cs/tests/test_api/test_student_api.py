"""Student API tests."""
from rest_framework import status
from tests.factory import StudentFactory, TutoringGroupFactory, UserFactory
from tests.test_api.mixins import ProfileEndpointsTestMixin
from tests.utils.api import HyperlinkedAPITestCase

from users.serializers import StudentSerializer


class StudentEndpointsTest(ProfileEndpointsTestMixin, HyperlinkedAPITestCase):
    """Test access to the students endpoints.

    Regular actions tests are provided by the ProfileEndpointsTestMixin.
    """

    factory = StudentFactory
    serializer_class = StudentSerializer

    def perform_list(self):
        response = self.client.get('/api/students/')
        return response

    def perform_retrieve(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        response = self.client.get('/api/students/{obj.pk}/'.format(obj=obj))
        return response

    def perform_create(self):
        url = '/api/students/'
        user = UserFactory.create()
        tutoring_group = TutoringGroupFactory.create()
        obj = self.factory.build(user=user,
                                 tutoring_group=tutoring_group,
                                 school=tutoring_group.school)
        data = self.serialize(obj, 'post', url)
        response = self.client.post(url, data, format='json')
        return response

    def perform_update(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = '/api/students/{obj.pk}/'.format(obj=obj)
        data = self.serialize(obj, 'put', url)
        data['address'] = 'Modified address'
        response = self.client.put(url, data, format='json')
        return response

    def perform_partial_update(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        response = self.client.patch('/api/students/{obj.pk}/'.format(obj=obj),
                                     data={'address': 'Modified address'},
                                     format='json')
        return response

    def perform_delete(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        response = self.client.delete(
            '/api/students/{obj.pk}/'.format(obj=obj))
        return response

    def test_retrieve_tutoring_group(self):
        def perform_retrieve_tutoring_group():
            obj = self.factory.create()
            response = self.client.get(
                '/api/students/{}/tutoringgroup/'.format(obj.pk))
            return response

        self.assertRequiresAuth(perform_retrieve_tutoring_group,
                                expected_status_code=status.HTTP_200_OK)
