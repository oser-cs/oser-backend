"""Visits serializers."""

from django.utils.timezone import now
from rest_framework import serializers

from core.markdown import MarkdownField
from core.serializers import AddressSerializer
from profiles.models import Tutor
from users.models import User
from users.serializers import UserSerializer

from .models import AttachedFile, Participation, Place, Visit


class PlaceSerializer(serializers.ModelSerializer):
    """Serializer for Place."""

    description = MarkdownField()
    address = AddressSerializer()

    class Meta:  # noqa
        model = Place
        fields = ('id', 'name', 'address', 'description')


class ParticipationSerializer(serializers.ModelSerializer):
    """Serializer for visit participations."""

    user = UserSerializer()

    class Meta:  # noqa
        model = Participation
        fields = ('id', 'user', 'present', 'accepted',)


class VisitOrganizerSerializer(serializers.ModelSerializer):
    """Serializer for visit organizers."""

    user = UserSerializer()

    class Meta:  # noqa
        model = Tutor
        fields = ('id', 'user',)


class AttachedFileSerializer(serializers.ModelSerializer):
    """Serializer for required attached files on visits."""

    class Meta:  # noqa
        model = AttachedFile
        fields = ('id', 'name', 'required')


class VisitListSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for lists of visits."""

    place = serializers.StringRelatedField()
    participants = serializers.SerializerMethodField()

    def get_participants(self, obj):
        return obj.participants.values_list('id', flat=True)

    organizers = serializers.SerializerMethodField()

    def get_organizers(self, obj):
        return obj.organizers.values_list('user__id', flat=True)

    passed = serializers.SerializerMethodField()

    def get_passed(self, obj: Visit) -> bool:
        """Return true if the visit already happened, false otherwise."""
        return obj.date < now()

    class Meta:  # noqa
        model = Visit
        fields = ('id', 'title', 'summary', 'place', 'date', 'deadline',
                  'passed', 'registrations_open', 'participants', 'organizers',
                  'image', 'url')
        extra_kwargs = {'url': {'view_name': 'api:visit-detail'}}


class VisitSerializer(VisitListSerializer):
    """Serializer for Visit."""

    participants = ParticipationSerializer(source='participations', many=True)
    place = PlaceSerializer()
    organizers = VisitOrganizerSerializer(many=True)
    attached_files = AttachedFileSerializer(many=True)

    class Meta(VisitListSerializer.Meta):  # noqa
        depth = 1
        fields = ('id', 'title', 'summary', 'description', 'place',
                  'date', 'deadline', 'passed', 'registrations_open',
                  'participants', 'organizers',
                  'attached_files', 'image', 'fact_sheet',
                  'url',)


class ParticipationWriteSerializer(serializers.ModelSerializer):
    """Serializer for adding participants to visits."""

    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.all(),
        help_text='Identifier for the user')
    visit_id = serializers.PrimaryKeyRelatedField(
        source='visit',
        queryset=Visit.objects.all(),
        help_text='Identifier for the visit')

    class Meta:  # noqa
        model = Participation
        fields = ('id', 'user_id', 'visit_id', 'present')


class ParticipationIdentifySerializer(serializers.ModelSerializer):
    """Serializer for the specialized get_id() view."""

    user_id = serializers.IntegerField()
    visit_id = serializers.IntegerField()

    class Meta:  # noqa
        model = Participation
        fields = ('user_id', 'visit_id',)
