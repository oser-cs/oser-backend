"""Users API serializers."""

from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for User.

    Actions: list, retrieve, update, partial_update, delete
    """

    date_of_birth = serializers.DateField()

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
        fields = ('id', 'url', 'email',
                  'first_name', 'last_name',
                  'phone_number', 'date_of_birth',)
        extra_kwargs = {
            'url': {'view_name': 'api:user-detail'},
            'email': {'read_only': True},
        }


class UserCreateSerializer(UserSerializer):
    """Serializer for creating users.

    Actions: create
    """

    date_of_birth = serializers.DateField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta(UserSerializer.Meta):  # noqa
        fields = (*UserSerializer.Meta.fields, 'password')
        extra_kwargs = {
            **UserSerializer.Meta.extra_kwargs,
            'email': {'read_only': False},
        }
