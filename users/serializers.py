"""Users serializers."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Hyperlinked serializer for user objects."""

    class Meta:  # noqa
        model = User
        fields = ('id', 'email', 'profile_type',
                  'first_name', 'last_name', 'phone_number', 'url',)
        extra_kwargs = {
            'email': {'read_only': True},
            'url': {'view_name': 'api:user-detail'},
        }
