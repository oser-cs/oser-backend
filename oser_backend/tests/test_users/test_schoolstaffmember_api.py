"""SchoolStaffMember API tests."""
from tests.utils import ProfileEndpointsTestMixin
from tests.utils.api import HyperlinkedAPITestCase
from tutoring.factory import SchoolFactory
from users.factory import SchoolStaffMemberFactory, UserFactory
from users.serializers import SchoolStaffMembersSerializer


class SchoolStaffMemberEndpointsTest(ProfileEndpointsTestMixin,
                                     HyperlinkedAPITestCase):
    """Test access to the school staff member endpoints.

    Regular actions tests are provided by the ProfileEndpointsTestMixin.
    """

    factory = SchoolStaffMemberFactory
    serializer_class = SchoolStaffMembersSerializer

    def perform_list(self):
        response = self.client.get('/api/schoolstaffmembers/')
        return response

    def perform_retrieve(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        response = self.client.get(
            '/api/schoolstaffmembers/{obj.pk}/'.format(obj=obj))
        return response

    def perform_create(self):
        url = '/api/schoolstaffmembers/'
        school = SchoolFactory.create()
        user = UserFactory.create()
        obj = self.factory.build(user=user)
        obj = self.factory.build(user=user, school=school)
        data = self.serialize(obj, 'post', url)
        response = self.client.post(url, data, format='json')
        return response

    def perform_update(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = '/api/schoolstaffmembers/{obj.pk}/'.format(obj=obj)
        data = self.serialize(obj, 'put', url)
        data['role'] = 'proviseur'
        response = self.client.put(url, data, format='json')
        return response

    def perform_partial_update(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = '/api/schoolstaffmembers/{obj.pk}/'.format(obj=obj)
        data = {'role': 'proviseur'}
        response = self.client.patch(url, data, format='json')
        return response

    def perform_delete(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = '/api/schoolstaffmembers/{obj.pk}/'.format(obj=obj)
        response = self.client.delete(url)
        return response
