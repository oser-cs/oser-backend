"""Projects serializers."""

from rest_framework import serializers

from users.fields import UserField
from users.serializers import UserSerializer

from .models import Edition, Participation, Project


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Project objects."""

    class Meta:  # noqa
        model = Project
        fields = ('id', 'url', 'name', 'description', 'logo')
        extra_kwargs = {
            'url': {'view_name': 'api:project-detail'},
        }


class ParticipationSerializer(serializers.ModelSerializer):
    """Serializer for project edition participations."""

    user = UserField(
        label='Utilisateur',
        help_text='Identifier for the user who participates.')

    edition = serializers.PrimaryKeyRelatedField(
        queryset=Edition.objects.all(),
        label='Édition',
        help_text='Identifier for the associated edition.')

    class Meta:  # noqa
        model = Participation
        fields = ('id', 'submitted', 'user', 'edition', 'state',)


class EditionSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Edition objects."""

    project = ProjectSerializer()
    organizers = UserSerializer(many=True)
    participations = ParticipationSerializer(many=True)

    class Meta:  # noqa
        model = Edition
        fields = ('id', 'url', 'name', 'year', 'project', 'description',
                  'organizers', 'participations')
        extra_kwargs = {
            'url': {'view_name': 'api:edition-detail'},
        }
