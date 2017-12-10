"""Persons API serializers."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from persons.models import Tutor, Student, SchoolStaffMember
from tutoring.models import TutoringGroup, School


class PersonSerializer(serializers.Serializer):
    """Base serializer for person models."""

    user = serializers.HyperlinkedRelatedField(
        queryset=get_user_model().objects.all(),
        view_name='api:user-detail',
    )


class TutorSerializer(PersonSerializer,
                      serializers.HyperlinkedModelSerializer):
    """Serializer for Tutor."""

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


class StudentSerializer(PersonSerializer,
                        serializers.HyperlinkedModelSerializer):
    """Serializer for Student."""

    school = serializers.HyperlinkedRelatedField(
        queryset=School.objects.all(),
        view_name='api:school-detail',
    )
    tutoring_group = serializers.HyperlinkedRelatedField(
        queryset=TutoringGroup.objects.all(),
        view_name='api:tutoringgroup-detail',
    )

    class Meta:  # noqa
        model = Student
        fields = ('user', 'address', 'tutoring_group', 'school',)
        extra_kwargs = {
            'url': {
                'view_name': 'api:student-detail',
            }
        }


class SchoolStaffMembersSerializer(PersonSerializer,
                                   serializers.HyperlinkedModelSerializer):
    """Serializer for SchoolStaffMembers."""

    school = serializers.HyperlinkedRelatedField(
        queryset=School.objects.all(),
        view_name='api:school-detail',
    )

    class Meta:  # noqa
        model = SchoolStaffMember
        fields = ('user', 'role', 'school',)
        extra_kwargs = {
            'url': {
                'view_name': 'api:schoolstaffmember-detail',
            }
        }
