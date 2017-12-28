"""Student API tests."""

from rest_framework import status

from users.serializers import StudentSerializer
from tests.factory import StudentFactory, UserFactory, TutoringGroupFactory
from tests.utils.api import HyperlinkedAPITestCase


class StudentEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the students endpoints."""

    factory = StudentFactory
    serializer_class = StudentSerializer

    def perform_list(self):
        response = self.client.get('/api/students/')
        return response

    def test_list_anonymous_is_forbidden(self):
        """Test anonymous users cannot list students."""
        self.assertForbidden(self.perform_list, user=None)

    def test_list_authenticated_is_allowed(self):
        """Test an authenticated user can list students."""
        self.assertAuthorized(self.perform_list, user=UserFactory.create(),
                              expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        response = self.client.get(f'/api/students/{obj.pk}/')
        return response

    def test_retrieve_anonymous_is_forbidden(self):
        """Test anonymous users cannot retrieve a student."""
        self.assertForbidden(self.perform_list, user=None)

    def test_retrieve_authenticated_is_allowed(self):
        """Test an authenticated user can retrieve a student."""
        self.assertAuthorized(self.perform_retrieve, user=UserFactory.create(),
                              expected_status_code=status.HTTP_200_OK)

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

    def test_create_anonymous_is_allowed(self):
        """Test anonymous users can create a new student.

        (Provided they are authenticated into the API.)
        """
        self.assertAuthorized(self.perform_create, user=None,
                              expected_status_code=status.HTTP_201_CREATED)

    def perform_update(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = f'/api/students/{obj.pk}/'
        data = self.serialize(obj, 'put', url)
        data['address'] = 'Modified address'
        response = self.client.put(url, data, format='json')
        return response

    def test_update_anonymous_is_forbidden(self):
        """Test anonymous users cannot update a student."""
        self.assertForbidden(self.perform_update, user=None)

    def test_update_authenticated_is_forbidden(self):
        """Test an authenticated user cannot update any student."""
        self.assertForbidden(self.perform_update, user=UserFactory.create())

    def test_update_authenticated_self_is_allowed(self):
        """Test an authenticated user can update its student profile."""
        obj = self.factory.create()
        user = obj.user
        self.assertAuthorized(lambda: self.perform_update(obj=obj), user=user,
                              expected_status_code=status.HTTP_200_OK)

    def perform_partial_update(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        response = self.client.patch(f'/api/students/{obj.pk}/',
                                     data={'address': 'Modified address'},
                                     format='json')
        return response

    def test_partial_update_anonymous_is_forbidden(self):
        """Test anonymous users cannot partially update a student."""
        self.assertForbidden(self.perform_partial_update, user=None)

    def test_partial_update_authenticated_is_forbidden(self):
        """Test an authenticated user cannot partially update any student."""
        self.assertForbidden(self.perform_partial_update,
                             user=UserFactory.create())

    def test_partial_update_authenticated_self_is_allowed(self):
        """Test authenticated user can partially update its student profile."""
        obj = self.factory.create()
        user = obj.user
        self.assertAuthorized(lambda: self.perform_partial_update(obj=obj),
                              user=user,
                              expected_status_code=status.HTTP_200_OK)

    def perform_delete(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        response = self.client.delete(f'/api/students/{obj.pk}/')
        return response

    def test_delete_anonymous_is_forbidden(self):
        """Test anonymous users cannot delete a student."""
        self.assertForbidden(self.perform_delete, user=None)

    def test_delete_authenticated_is_forbidden(self):
        """Test an authenticated user cannot delete any student."""
        self.assertForbidden(self.perform_delete,
                             user=UserFactory.create())

    def test_delete_authenticated_self_is_allowed(self):
        """Test authenticated user can delete its student profile."""
        obj = self.factory.create()
        user = obj.user
        self.assertAuthorized(lambda: self.perform_delete(obj=obj),
                              user=user,
                              expected_status_code=status.HTTP_204_NO_CONTENT)

    def test_retrieve_tutoring_group(self):
        pass  # TODO
