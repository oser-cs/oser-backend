"""Users API serializers."""

from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User."""

    date_of_birth = serializers.DateField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
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
        fields = ('id', 'email', 'password',
                  'first_name', 'last_name',
                  'phone_number', 'date_of_birth',)
