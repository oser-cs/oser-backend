"""Visits serializers."""

from django.utils.timezone import now
from rest_framework import serializers

from core.markdown import MarkdownField
from users.models import User

from .models import Place, Visit, VisitParticipant


class PlaceSerializer(serializers.ModelSerializer):
    """Serializer for Place."""

    description = MarkdownField()

    class Meta:  # noqa
        model = Place
        fields = ('id', 'name', 'address', 'description')


class VisitOrganizerSerializer(serializers.ModelSerializer):

    class Meta:  # noqa
        model = User
        fields = ('id', 'first_name', 'last_name', 'gender', 'phone_number')


class VisitSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Visit."""

    participants = serializers.StringRelatedField(many=True)
    passed = serializers.SerializerMethodField()
    place = PlaceSerializer(read_only=True)
    organizers = VisitOrganizerSerializer(source='organizers_group.user_set',
                                          read_only=True,
                                          many=True)

    def get_passed(self, obj):
        return obj.date < now()

    class Meta:  # noqa
        model = Visit
        fields = ('id', 'url', 'title', 'summary', 'description', 'place',
                  'date', 'passed',
                  'deadline', 'registrations_open',
                  'participants',
                  'organizers',
                  'image',
                  'fact_sheet',)
        extra_kwargs = {
            'url': {'view_name': 'api:visit-detail'},
        }


class VisitParticipantReadSerializer(serializers.HyperlinkedModelSerializer):
    """Readable serializer for visit participants."""

    user = serializers.HyperlinkedRelatedField(
        'api:user-detail',
        read_only=True,
    )
    visit = serializers.HyperlinkedRelatedField(
        'api:visit-detail',
        read_only=True,
    )

    class Meta:  # noqa
        model = VisitParticipant
        fields = ('id', 'url', 'user', 'visit', 'present')
        extra_kwargs = {
            'url': {'view_name': 'api:visit-participants-detail'},
        }


class VisitParticipantWriteSerializer(serializers.ModelSerializer):
    """Writable serializer for visit participants."""

    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.all(),
        help_text='Identifier for the user')
    visit_id = serializers.PrimaryKeyRelatedField(
        source='visit',
        queryset=Visit.objects.all(),
        help_text='Identifier for the visit')

    class Meta:  # noqa
        model = VisitParticipant
        fields = ('id', 'user_id', 'visit_id', 'present')


class VisitParticipantDetailSerializer(serializers.ModelSerializer):
    """Serializer with detailed information about visit participants."""

    user_id = serializers.PrimaryKeyRelatedField(
        source='user.id',
        queryset=User.objects.all(),
        label='Utilisateur')
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    last_name = serializers.CharField(
        source='user.last_name', read_only=True)
    phone_number = serializers.CharField(
        source='user.phone_number', read_only=True)
    email = serializers.EmailField(source='user.email',
                                   read_only=True)

    class Meta:  # noqa
        model = VisitParticipant
        fields = ('user_id', 'first_name', 'last_name',
                  'phone_number', 'email', 'present',)


class VisitParticipantIdentifySerializer(serializers.ModelSerializer):
    """Serializer for the specialized get_id() view."""

    user_id = serializers.IntegerField()
    visit_id = serializers.IntegerField()

    class Meta:  # noqa
        model = VisitParticipant
        fields = ('user_id', 'visit_id',)
