"""Student API tests."""

from rest_framework import status

from users.serializers import StudentSerializer
from tests.factory import StudentFactory, UserFactory, TutoringGroupFactory
from tests.utils.api import HyperlinkedAPITestCase


class StudentEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the students endpoints."""

    factory = StudentFactory
    serializer_class = StudentSerializer

    def test_list(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        obj = self.factory.create()
        response = self.client.get(f'/api/students/{obj.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        url = '/api/students/'
        user = UserFactory.create()
        tutoring_group = TutoringGroupFactory.create()
        obj = self.factory.build(user=user,
                                 tutoring_group=tutoring_group,
                                 school=tutoring_group.school)
        data = self.serialize(obj, 'post', url)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         response.data)

    def test_update(self):
        obj = self.factory.create()
        url = f'/api/students/{obj.pk}/'
        data = self.serialize(obj, 'put', url)
        data['address'] = 'Modified address'
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        obj = self.factory.create()
        response = self.client.patch(f'/api/students/{obj.pk}/',
                                     data={'address': 'Modified address'},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        obj = self.factory.create()
        response = self.client.delete(f'/api/students/{obj.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
