"""Tutoring API serializers."""

from rest_framework import serializers

from profiles.models import Student
from core.serializers import AddressSerializer

from .models import School, TutoringGroup, TutoringSession


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for School.

    Suited for: list, retrieve, update, partial_update, delete
    """

    address = AddressSerializer()
    students = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Student.objects.all(),
        help_text='Lycéens inscrits à ce lycée',
    )
    students_count = serializers.IntegerField(source='students.count',
                                              read_only=True)

    class Meta:  # noqa
        model = School
        fields = ('uai_code', 'name', 'address', 'students',
                  'students_count', 'url',)
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


class TutoringGroupSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for TutoringGroup."""

    tutors = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )
    students = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )
    school = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    students_count = serializers.IntegerField(source='students.count',
                                              read_only=True)
    tutors_count = serializers.IntegerField(source='tutors.count',
                                            read_only=True)

    class Meta:  # noqa
        model = TutoringGroup
        fields = ('id', 'name', 'tutors', 'students', 'school',
                  'students_count', 'tutors_count', 'url',)
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
        fields = ('id', 'date', 'start_time', 'end_time',
                  'tutoring_group', 'url',)
        extra_kwargs = {
            'url': {'view_name': 'api:tutoring_session-detail'},
        }
