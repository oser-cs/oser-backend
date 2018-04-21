"""Users API serializers."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.serializers import AddressSerializer
from tutoring.models import School, TutoringGroup

from .models import Student, Tutor

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Hyperlinked serializer for User.

    Actions: list, retrieve, delete
    """

    class Meta:  # noqa
        model = User
        fields = ('id', 'email', 'profile_type',
                  'first_name', 'last_name',
                  'gender',
                  'phone_number', 'date_of_birth', 'url',)
        extra_kwargs = {
            'email': {'read_only': True},
            'url': {'view_name': 'api:user-detail'},
        }


class TutorSerializer(serializers.HyperlinkedModelSerializer):
    """Hyperlinked serializer for Tutor."""

    user = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        view_name='api:user-detail',
    )
    tutoring_groups = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:tutoring_group-detail',
    )

    class Meta:  # noqa
        model = Tutor
        fields = ('user_id', 'user', 'promotion', 'tutoring_groups', 'url',)
        extra_kwargs = {
            'url': {'view_name': 'api:tutor-detail'},
        }


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    """Hyperlinked serializer for Student."""

    user = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        view_name='api:user-detail',
    )
    tutoring_group = serializers.HyperlinkedRelatedField(
        queryset=TutoringGroup.objects.all(),
        view_name='api:student-tutoringgroup',
    )
    school = serializers.HyperlinkedRelatedField(
        queryset=School.objects.all(),
        view_name='api:school-detail',
    )
    visits = serializers.HyperlinkedRelatedField(
        source='user.visit_set',
        many=True,
        view_name='api:visit-detail',
        read_only=True)
    address = AddressSerializer()

    class Meta:  # noqa
        model = Student
        fields = ('user_id', 'url', 'user', 'address', 'tutoring_group',
                  'school', 'visits',)
        extra_kwargs = {
            'url': {'view_name': 'api:student-detail'},
        }
