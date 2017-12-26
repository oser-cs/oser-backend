"""Tutoring API serializers."""

from rest_framework import serializers

from .models import (
    TutoringGroup, School, TutoringSession)
from users.models import Student


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for School.

    Suited for: list, retrieve, update, partial_update, delete
    """

    students = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Student.objects.all(),
        view_name='api:student-detail',
        help_text='Lycéens inscrits à ce lycée',
    )
    students_count = serializers.IntegerField(source='students.count',
                                              read_only=True)

    class Meta:  # noqa
        model = School
        fields = ('uai_code', 'url', 'name', 'address', 'students',
                  'students_count',)
        extra_kwargs = {
            'url': {'view_name': 'api:school-detail'},
            'uai_code': {'read_only': True},
        }

    @staticmethod
    def setup_eager_loading(queryset):
        """Setup eager loading in advance.

        Prevents the N+1 query problem by pre-fetching the students.

        Source: http://ses4j.github.io/2015/11/23/
                optimizing-slow-django-rest-framework-performance
        """
        queryset = queryset.prefetch_related('students')
        return queryset


class SchoolCreateSerializer(SchoolSerializer):
    """Serializer for creating new school instances.

    Suited for: create
    """

    students = serializers.HyperlinkedRelatedField(
        many=True,
        required=False,
        queryset=Student.objects.all(),
        view_name='api:student-detail',
        help_text='Lycéens inscrits à ce lycée',
    )

    class Meta(SchoolSerializer.Meta):  # noqa
        extra_kwargs = {
            **SchoolSerializer.Meta.extra_kwargs,
            'uai_code': {'read_only': False},
        }


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
    school = serializers.HyperlinkedRelatedField(
        queryset=School.objects.all(),
        view_name='api:school-detail',
    )
    students_count = serializers.IntegerField(source='students.count',
                                              read_only=True)
    tutors_count = serializers.IntegerField(source='tutors.count',
                                            read_only=True)

    class Meta:  # noqa
        model = TutoringGroup
        fields = ('id', 'url', 'name', 'tutors', 'students', 'school',
                  'students_count', 'tutors_count',)
        extra_kwargs = {
            'url': {'view_name': 'api:tutoring_group-detail'},
        }

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('school')
        queryset = queryset.prefetch_related('tutors')
        queryset = queryset.prefetch_related('students')
        return queryset


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
