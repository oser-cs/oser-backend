"""API test mixins."""

from rest_framework import status


class ProfileEndpointsTestMixin:
    """Test access to the profile endpoints."""

    factory = None
    serializer_class = None

    def test_list_requires_to_be_authenticated(self):
        """Test user needs to be authenticated to list profiles."""
        self.assertRequiresAuth(self.perform_list,
                                expected_status_code=status.HTTP_200_OK)

    def test_retrieve_requires_to_be_authenticated(self):
        """Test user needs to be authenticated to retrieve a profile."""
        self.assertRequiresAuth(self.perform_retrieve,
                                expected_status_code=status.HTTP_200_OK)

    def test_create_anonymous_is_allowed(self):
        """Test anonymous users can create a new profile.

        (Provided they are authenticated into the API.)
        """
        self.assertRequestResponse(
            self.perform_create, user=None,
            expected_status_code=status.HTTP_201_CREATED)

    # update action

    def test_update_authenticated_is_forbidden(self):
        """Test an authenticated user cannot update any profile."""
        self.assertAuthForbidden(self.perform_update)

    def test_update_authenticated_self_is_allowed(self):
        """Test an authenticated user can update their own profile."""
        obj = self.factory.create()
        user = obj.user
        self.assertRequestResponse(
            lambda: self.perform_update(obj=obj), user=user,
            expected_status_code=status.HTTP_200_OK)

    # partial update action

    def test_partial_update_authenticated_is_forbidden(self):
        """Test authenticated user cannot partially update any profile."""
        self.assertAuthForbidden(self.perform_partial_update)

    def test_partial_update_authenticated_self_is_allowed(self):
        """Test an authenticated user can partially update their profile."""
        obj = self.factory.create()
        user = obj.user
        self.assertRequestResponse(
            lambda: self.perform_partial_update(obj=obj),
            user=user,
            expected_status_code=status.HTTP_200_OK)

    # delete action

    def test_delete_authenticated_is_forbidden(self):
        """Test authenticated user cannot delete any school staff member."""
        self.assertAuthForbidden(self.perform_delete)

    def test_delete_authenticated_self_is_allowed(self):
        """Test authenticated school staff member can delete its profile."""
        obj = self.factory.create()
        user = obj.user
        self.assertRequestResponse(
            lambda: self.perform_delete(obj=obj),
            user=user,
            expected_status_code=status.HTTP_204_NO_CONTENT)


class SimpleReadOnlyResourceTestMixin:
    """Test mixin for simple read-only resources.

    Must be mixed in with a SimpleAPITestCase.

    Provided tests check the following:
    - the list action is not authenticated, and returns code 200
    - the retrieve action is not authenticated, and returns code 200
    """

    list_url: str
    retrieve_url_fmt: str

    # Optional kwargs passed to factory.create() in perform_retrieve()
    retrieve_kwargs = {}

    def perform_list(self):
        response = self.client.get(self.list_url)
        return response

    def test_list_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_list,
            user=None,
            expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create(**self.retrieve_kwargs)
        url = self.retrieve_url_fmt.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_retrieve,
            user=None,
            expected_status_code=status.HTTP_200_OK)
