"""Persons API serializers."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from persons.models import Tutor, Student
from tutoring.models import TutoringGroup


class TutorSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Tutor."""

    user = serializers.HyperlinkedRelatedField(
        queryset=get_user_model().objects.all(),
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


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Student."""

    user = serializers.HyperlinkedRelatedField(
        queryset=get_user_model().objects.all(),
        view_name='api:user-detail',
    )

    tutoring_group = serializers.HyperlinkedRelatedField(
        queryset=TutoringGroup.objects.all(),
        view_name='api:tutoringgroup-detail',
    )

    class Meta:  # noqa
        model = Student
        fields = ('user', 'address', 'tutoring_group',)
        extra_kwargs = {
            'url': {
                'view_name': 'api:student-detail',
            }
        }
