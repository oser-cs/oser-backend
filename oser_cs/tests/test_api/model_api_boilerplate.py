"""Model API tests."""

from rest_framework import status

# from tests.factory import ***
# from xxx.serializers import ***
from tests.utils.api import HyperlinkedAPITestCase


class StudentEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the students endpoints."""

    factory = 'StudentFactory'
    serializer_class = 'StudentSerializer'

    def test_list(self):
        url = ''
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        obj = self.factory.create()
        url = '/api/foo/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        url = '/api/students/'
        # build obj using factory.build()
        obj = self.factory.build()
        # serialize the object to get POST data
        data = self.serialize(obj, 'post', url)
        # send request and check status code
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         msg=response.data)

    def test_update(self):
        # create test obj
        obj = self.factory.create()
        # PUT request URL
        url = '/api/foo/{obj.pk}/'.format(obj=obj)
        # serialize the object to get PUT data
        data = self.serialize(obj, 'put', url)
        # update one of the fields
        field = 'address'
        field_value = 'Modified address'
        data[field] = field_value
        # send request and check status code
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         msg=response.data)

    def test_partial_update(self):
        # create test obj
        obj = self.factory.create()
        # PATCH request URL
        url = '/api/foo/{obj.pk}/'.format(obj=obj)
        # update one of the fields
        field = 'address'
        field_value = 'Modified address'
        data = []
        data[field] = field_value
        # send request and check status code
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         msg=response.data)

    def test_delete(self):
        # create test obj
        obj = self.factory.create()
        # DELETE request URL
        url = '/api/foo/{obj.pk}/'.format(obj=obj)
        # send request and check status code
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
