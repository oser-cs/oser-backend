"""Student API tests."""
from users.serializers import StudentSerializer
from tests.factory import StudentFactory, UserFactory, TutoringGroupFactory
from tests.utils.api import HyperlinkedAPITestCase
from tests.test_api.mixins import ProfileEndpointsTestMixin


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
        response = self.client.get(f'/api/students/{obj.pk}/')
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
        url = f'/api/students/{obj.pk}/'
        data = self.serialize(obj, 'put', url)
        data['address'] = 'Modified address'
        response = self.client.put(url, data, format='json')
        return response

    def perform_partial_update(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        response = self.client.patch(f'/api/students/{obj.pk}/',
                                     data={'address': 'Modified address'},
                                     format='json')
        return response

    def perform_delete(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        response = self.client.delete(f'/api/students/{obj.pk}/')
        return response

    def test_retrieve_tutoring_group(self):
        pass  # TODO
