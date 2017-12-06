"""API serializers."""

from rest_framework import serializers
from users.models import User
from persons.models import Tutor
from tutoring.models import TutoringGroup


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


class TutorSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Tutor."""

    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='api:user-detail',
    )
    tutoring_groups = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:tutoringgroup-detail',
    )

    class Meta:  # noqa
        model = Tutor
        fields = ('user', 'promotion', 'tutoring_groups',)
        extra_kwargs = {
            'url': {
                'view_name': 'api:tutor-detail',
            }
        }


class TutoringGroupSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for TutoringGroup."""

    tutors = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:tutor-detail',
    )

    class Meta:  # noqa
        model = TutoringGroup
        fields = ('name', 'tutors',)
        extra_kwargs = {
            'url': {
                'view_name': 'api:tutoringgroup-detail',
            }
        }
