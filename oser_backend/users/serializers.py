"""Users API serializers."""

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from rest_framework import serializers
from .models import Tutor, Student, SchoolStaffMember
from tutoring.models import School, TutoringGroup
from visits.models import Visit
from visits.serializers import VisitSerializer

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Hyperlinked serializer for User.

    Actions: list, retrieve, delete
    """

    profile = serializers.SerializerMethodField(read_only=True)

    def get_profile(self, obj):
        try:
            profile = obj.profile
            request = self.context['request']
            url = request.build_absolute_uri(profile.get_absolute_url())
            return url
        except AttributeError:
            return None

    class Meta:  # noqa
        model = User
        fields = ('id', 'email',
                  'first_name', 'last_name',
                  'gender',
                  'phone_number', 'date_of_birth',
                  'profile', 'url',)
        extra_kwargs = {
            'email': {'read_only': True},
            'url': {'view_name': 'api:user-detail'},
        }


class UserCreateSerializer(UserSerializer):
    """Serializer for creating users.

    Actions: create
    """

    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta(UserSerializer.Meta):  # noqa
        fields = (*UserSerializer.Meta.fields,
                  'profile_type', 'password',)
        extra_kwargs = {
            **UserSerializer.Meta.extra_kwargs,
            'email': {'read_only': False},
        }


class UserUpdateSerializer(UserSerializer):
    """Serializer for updating users.

    Actions: update, partial_update
    """

    class Meta(UserSerializer.Meta):  # noqa
        extra_kwargs = {
            **UserSerializer.Meta.extra_kwargs,
            'email': {'read_only': False},
        }


class ProfileSerializer(serializers.Serializer):
    """Base hyperlinked serializer for profile models."""

    user = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        view_name='api:user-detail',
    )


class TutorSerializer(ProfileSerializer,
                      serializers.HyperlinkedModelSerializer):
    """Hyperlinked serializer for Tutor."""

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


class StudentSerializer(ProfileSerializer,
                        serializers.HyperlinkedModelSerializer):
    """Hyperlinked serializer for Student."""

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

    class Meta:  # noqa
        model = Student
        fields = ('user_id', 'url', 'user', 'address', 'tutoring_group',
                  'school', 'visits',)
        extra_kwargs = {
            'url': {'view_name': 'api:student-detail'},
        }


class SchoolStaffMembersSerializer(ProfileSerializer,
                                   serializers.HyperlinkedModelSerializer):
    """Serializer for SchoolStaffMembers."""

    school = serializers.HyperlinkedRelatedField(
        queryset=School.objects.all(),
        view_name='api:school-detail',
    )

    class Meta:  # noqa
        model = SchoolStaffMember
        fields = ('user_id', 'url', 'user', 'role', 'school',)
        extra_kwargs = {
            'url': {'view_name': 'api:schoolstaffmember-detail'},
        }
