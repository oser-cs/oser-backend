"""Users API serializers."""

from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for User."""

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data.get('email'),
            # TODO add User custom fields
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        for field in validated_data:
            if field == 'password':
                instance.set_password(validated_data.get('password'))
            else:
                setattr(instance, field, validated_data.get(field))
        instance.save()
        return instance

    class Meta:  # noqa
        model = User
        fields = ('url', 'id', 'email', 'password',
                  'first_name', 'last_name',
                  'phone_number', 'date_of_birth',)
        extra_kwargs = {
            'url': {
                'view_name': 'api:user-detail',
            }
        }
