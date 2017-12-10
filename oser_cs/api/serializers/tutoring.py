"""Tutoring API serializers."""

from rest_framework import serializers
from tutoring.models import TutoringGroup, School, TutoringSession
from persons.models import Student


class TutoringGroupSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for TutoringGroup."""

    tutors = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:tutor-detail',
    )
    students = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:student-detail',
    )

    class Meta:  # noqa
        model = TutoringGroup
        fields = ('name', 'tutors', 'students')
        extra_kwargs = {
            'url': {
                'view_name': 'api:tutoring_group-detail',
            }
        }


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for School."""

    students = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Student.objects.all(),
        view_name='api:student-detail',
    )

    class Meta:  # noqa
        model = School
        fields = ('uai_code', 'name', 'students',)
        extra_kwargs = {
            'url': {
                'view_name': 'api:school-detail',
            }
        }


class TutoringSessionSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for TutoringSession."""

    tutoring_group = serializers.HyperlinkedRelatedField(
        queryset=TutoringGroup.objects.all(),
        view_name='api:tutoring_group-detail',
    )

    class Meta:  # noqa
        model = TutoringSession
        fields = ('id', 'date', 'start_time', 'end_time', 'tutoring_group',)
        extra_kwargs = {
            'url': {
                'view_name': 'api:tutoring_session-detail',
            }
        }
