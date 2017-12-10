"""Tutoring API serializers."""

from rest_framework import serializers

from persons.models import Student, Tutor
from tutoring.models import TutoringGroup, School, TutoringSession


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for School."""

    students = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Student.objects.all(),
        view_name='api:student-detail',
    )

    class Meta:  # noqa
        model = School
        fields = ('uai_code', 'url', 'name', 'students',)
        extra_kwargs = {
            'url': {'view_name': 'api:school-detail'},
        }


class TutoringGroupSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for TutoringGroup."""

    tutors = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Tutor.objects.all(),
        view_name='api:tutor-detail',
    )
    students = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Student.objects.all(),
        view_name='api:student-detail',
    )
    school = serializers.HyperlinkedRelatedField(
        queryset=School.objects.all(),
        view_name='api:school-detail',
    )

    class Meta:  # noqa
        model = TutoringGroup
        fields = ('id', 'url', 'name', 'tutors', 'students', 'school',)
        extra_kwargs = {
            'url': {'view_name': 'api:tutoring_group-detail'},
        }


class TutoringSessionSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for TutoringSession."""

    tutoring_group = serializers.HyperlinkedRelatedField(
        queryset=TutoringGroup.objects.all(),
        view_name='api:tutoring_group-detail',
    )

    class Meta:  # noqa
        model = TutoringSession
        fields = ('id', 'url', 'date', 'start_time', 'end_time',
                  'tutoring_group',)
        extra_kwargs = {
            'url': {'view_name': 'api:tutoring_session-detail'},
        }
