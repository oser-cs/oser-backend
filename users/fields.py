"""Users fields."""

from rest_framework import serializers
from .serializers import UserSerializer
from .models import User


class UserField(serializers.Field):
    """A field for representing a user.

    Takes as input a user ID (for write operations)
    and outputs complete user profile information.
    """

    def to_internal_value(self, user_id: int) -> User:
        """Write from an ID as a user."""
        return User.objects.get(id=user_id)

    def to_representation(self, user: User) -> dict:
        """Read from a user as serialized user data."""
        request = self.context['request']
        return UserSerializer(user, context={'request': request}).data
