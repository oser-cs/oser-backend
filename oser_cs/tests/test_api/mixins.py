"""API test mixins."""
from rest_framework import status
from tests.factory import UserFactory


class ProfileEndpointsTestMixin:
    """Test access to the profile endpoints."""

    factory = None
    serializer_class = None

    # list action

    def test_list_anonymous_is_forbidden(self):
        """Test anonymous users cannot list profiles."""
        self.assertForbidden(self.perform_list, user=None)

    def test_list_authenticated_is_allowed(self):
        """Test an authenticated user can list profiles."""
        self.assertAuthorized(self.perform_list, user=UserFactory.create(),
                              expected_status_code=status.HTTP_200_OK)

    # retrieve action

    def test_retrieve_anonymous_is_forbidden(self):
        """Test anonymous users cannot retrieve a profile."""
        self.assertForbidden(self.perform_list, user=None)

    def test_retrieve_authenticated_is_allowed(self):
        """Test an authenticated user can retrieve a profile."""
        self.assertAuthorized(self.perform_retrieve, user=UserFactory.create(),
                              expected_status_code=status.HTTP_200_OK)

    # create action
    def test_create_anonymous_is_allowed(self):
        """Test anonymous users can create a new profile.

        (Provided they are authenticated into the API.)
        """
        self.assertAuthorized(self.perform_create, user=None,
                              expected_status_code=status.HTTP_201_CREATED)

    # update action

    def test_update_anonymous_is_forbidden(self):
        """Test anonymous users cannot update a profile."""
        self.assertForbidden(self.perform_update, user=None)

    def test_update_authenticated_is_forbidden(self):
        """Test an authenticated user cannot update any profile."""
        self.assertForbidden(self.perform_update, user=UserFactory.create())

    def test_update_authenticated_self_is_allowed(self):
        """Test an authenticated user can update their own profile."""
        obj = self.factory.create()
        user = obj.user
        self.assertAuthorized(lambda: self.perform_update(obj=obj), user=user,
                              expected_status_code=status.HTTP_200_OK)

    # partial update action

    def test_partial_update_anonymous_is_forbidden(self):
        """Test anonymous users cannot partially update a profile."""
        self.assertForbidden(self.perform_partial_update, user=None)

    def test_partial_update_authenticated_is_forbidden(self):
        """Test authenticated user cannot partially update any profile."""
        self.assertForbidden(self.perform_partial_update,
                             user=UserFactory.create())

    def test_partial_update_authenticated_self_is_allowed(self):
        """Test an authenticated user can partially update their profile."""
        obj = self.factory.create()
        user = obj.user
        self.assertAuthorized(lambda: self.perform_partial_update(obj=obj),
                              user=user,
                              expected_status_code=status.HTTP_200_OK)

    # delete action

    def test_delete_anonymous_is_forbidden(self):
        """Test anonymous users cannot delete a school staff member."""
        self.assertForbidden(self.perform_delete, user=None)

    def test_delete_authenticated_is_forbidden(self):
        """Test an authenticated user cannot delete any school staff member."""
        self.assertForbidden(self.perform_delete,
                             user=UserFactory.create())

    def test_delete_authenticated_self_is_allowed(self):
        """Test authenticated school staff member can delete its profile."""
        obj = self.factory.create()
        user = obj.user
        self.assertAuthorized(lambda: self.perform_delete(obj=obj),
                              user=user,
                              expected_status_code=status.HTTP_204_NO_CONTENT)
