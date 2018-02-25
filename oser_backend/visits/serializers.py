"""Visits serializers."""

from django.utils.timezone import now
from rest_framework import serializers

from users.models import Student

from .models import Visit, VisitParticipant, Place


class PlaceSerializer(serializers.ModelSerializer):

    class Meta:  # noqa
        model = Place
        fields = ('id', 'name', 'address')


class VisitSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Visit."""

    participants = serializers.StringRelatedField(many=True)
    passed = serializers.SerializerMethodField()
    place = PlaceSerializer(read_only=True)

    def get_passed(self, obj):
        return obj.date < now()

    class Meta:  # noqa
        model = Visit
        fields = ('id', 'url', 'title', 'summary', 'description', 'place',
                  'date', 'passed',
                  'deadline', 'registrations_open',
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
            'url': {'view_name': 'api:visit-participants-detail'},
        }


class VisitParticipantWriteSerializer(serializers.ModelSerializer):
    """Writable serializer for visit participants."""

    student_id = serializers.PrimaryKeyRelatedField(
        source='student',
        queryset=Student.objects.all(),
        help_text='Identifier for the student')
    visit_id = serializers.PrimaryKeyRelatedField(
        source='visit',
        queryset=Visit.objects.all(),
        help_text='Identifier for the visit')

    class Meta:  # noqa
        model = VisitParticipant
        fields = ('id', 'student_id', 'visit_id', 'present')


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


class VisitParticipantIdentifySerializer(serializers.ModelSerializer):

    student_id = serializers.IntegerField()
    visit_id = serializers.IntegerField()

    class Meta:  # noqa
        model = VisitParticipant
        fields = ('student_id', 'visit_id',)
