"""Tutor API tests."""

from rest_framework import status

from users.serializers import TutorSerializer
from tests.factory import TutorFactory
from tests.utils.api import HyperlinkedAPITestCase


class TutorEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the tutors endpoints."""

    factory = TutorFactory
    serializer_class = TutorSerializer

    def test_list(self):
        url = '/api/tutors/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        obj = self.factory.create()
        url = '/api/tutors/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        url = '/api/tutors/'
        obj = self.factory.build()
        data = self.serialize(obj, 'post', url)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         msg=response.data)

    def test_update(self):
        obj = self.factory.create()
        url = '/api/tutors/{obj.pk}/'.format(obj=obj)
        data = self.serialize(obj, 'put', url)
        data['promotion'] = 2020
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         msg=response.data)

    def test_partial_update(self):
        obj = self.factory.create()
        url = '/api/tutors/{obj.pk}/'.format(obj=obj)
        data = {'promotion': 2020}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         msg=response.data)

    def test_delete(self):
        obj = self.factory.create()
        url = '/api/tutors/{obj.pk}/'.format(obj=obj)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
