"""Visits serializers."""

from rest_framework import serializers
from .models import Visit, VisitParticipant
from users.models import Student


class VisitSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Visit."""

    participants = serializers.StringRelatedField(many=True)

    class Meta:  # noqa
        model = Visit
        fields = ('id', 'url', 'title', 'summary', 'description',
                  'place', 'date', 'deadline',
                  'registrations_open',
                  'participants',
                  'image', 'fact_sheet',)
        extra_kwargs = {
            'url': {'view_name': 'api:visit-detail'},
        }


class VisitParticipantReadSerializer(serializers.HyperlinkedModelSerializer):
    """Readable serializer for visit participants."""

    student = serializers.HyperlinkedRelatedField(
        'api:student-detail',
        read_only=True,
    )
    visit = serializers.HyperlinkedRelatedField(
        'api:visit-detail',
        read_only=True,
    )

    class Meta:  # noqa
        model = VisitParticipant
        fields = ('id', 'url', 'student', 'visit', 'present')
        extra_kwargs = {
            'url': {'view_name': 'api:visitparticipant-detail'}
        }


class VisitParticipantWriteSerializer(serializers.HyperlinkedModelSerializer):
    """Writable serializer for visit participants."""

    student = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Student.objects.all())
    visit = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Visit.objects.all())

    class Meta:  # noqa
        model = VisitParticipant
        fields = ('id', 'student', 'visit', 'present')


class VisitParticipantDetailSerializer(serializers.ModelSerializer):
    """Serializer with detailed information about visit participants."""

    student_id = serializers.PrimaryKeyRelatedField(
        source='student.id',
        queryset=Student.objects.all(),
        label='Lycéen')
    first_name = serializers.CharField(
        source='student.user.first_name', read_only=True)
    last_name = serializers.CharField(
        source='student.user.last_name', read_only=True)
    phone_number = serializers.CharField(
        source='student.user.phone_number', read_only=True)
    email = serializers.EmailField(source='student.user.email',
                                   read_only=True)

    class Meta:  # noqa
        model = VisitParticipant
        fields = ('student_id', 'first_name', 'last_name',
                  'phone_number', 'email', 'present',)
