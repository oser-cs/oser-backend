"""Tutoring API serializers."""

from rest_framework import serializers
from tutoring.models import TutoringGroup, School


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
                'view_name': 'api:tutoringgroup-detail',
            }
        }


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for School."""

    students = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
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
