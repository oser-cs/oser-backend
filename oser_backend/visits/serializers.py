"""Visits serializers."""

from django.utils.timezone import now
from rest_framework import serializers

from core.markdown import MarkdownField
from core.serializers import AddressSerializer
from profiles.models import Tutor
from users.models import User
from users.serializers import UserSerializer

from .notifications import ParticipationCancelled
from .models import Participation, Place, Visit


class PlaceSerializer(serializers.ModelSerializer):
    """Serializer for Place."""

    description = MarkdownField()
    address = AddressSerializer()

    class Meta:  # noqa
        model = Place
        fields = ('id', 'name', 'address', 'description')


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


class UserField(serializers.Field):
    """Custom user field used by ParticipationSerializer."""

    def to_internal_value(self, user_id: int) -> User:
        """Write from an ID as a user."""
        return User.objects.get(id=user_id)

    def to_representation(self, user: User) -> dict:
        """Read from a user as serialized user data."""
        request = self.context['request']
        return UserSerializer(user, context={'request': request}).data


class ParticipationSerializer(serializers.ModelSerializer):
    """Serializer for visit participations."""

    user = UserField(
        label='Utilisateur',
        help_text='Identifier for the user that participates.')
    visit = serializers.PrimaryKeyRelatedField(
        queryset=Visit.objects.all(),
        label='Sortie',
        help_text='Identifier for the associated visit.')

    class Meta:  # noqa
        model = Participation
        fields = ('id', 'user', 'visit', 'present', 'accepted',)


class VisitOrganizerSerializer(serializers.ModelSerializer):
    """Serializer for visit organizers."""

    user = UserSerializer()

    class Meta:  # noqa
        model = Tutor
        fields = ('id', 'user',)


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
        return obj.date < now().date() and obj.end_time < now().time()

    class Meta:  # noqa
        model = Visit
        fields = (
            'id', 'title', 'summary',
            'place', 'date', 'start_time', 'end_time',
            'deadline', 'passed', 'registrations_open',
            'participants', 'organizers',
            'image', 'url')
        extra_kwargs = {'url': {'view_name': 'api:visit-detail'}}


class VisitSerializer(VisitListSerializer):
    """Serializer for Visit."""

    participants = ParticipationSerializer(source='participations', many=True)
    place = PlaceSerializer()
    organizers = VisitOrganizerSerializer(many=True)

    class Meta(VisitListSerializer.Meta):  # noqa
        depth = 1
        fields = (
            'id', 'title', 'summary', 'description',
            'place', 'date', 'start_time', 'end_time', 'meeting',
            'deadline', 'passed', 'registrations_open',
            'participants', 'organizers',
            'image', 'fact_sheet', 'permission',
            'url',)


class ParticipationCancelledSerializer(serializers.Serializer):
    """Serializer for sending participation cancelled notifications."""

    reason = serializers.CharField(
        write_only=True,
        label='Reason',
        help_text='Explain why the user cancelled their participation.')

    sent = serializers.BooleanField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

    def update(self, instance: Participation, validated_data):
        """Send a notification as the user cancelled their participation."""
        reason = validated_data['reason']

        notification = ParticipationCancelled(
            user=instance.user, visit=instance.visit, reason=reason)
        notification.send()

        return notification

    class Meta:  # noqa
        model = Participation
