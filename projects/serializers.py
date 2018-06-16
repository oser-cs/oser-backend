"""Projects serializers."""

from rest_framework import serializers

from core.fields import MarkdownField
from users.fields import UserField
from users.serializers import UserSerializer
from profiles.serializers import TutorSerializer
from dynamicforms.serializers import FormDetailSerializer

from .models import Edition, Participation, Project, EditionForm


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Project objects."""

    description = MarkdownField()

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
        extra_kwargs = {
            'state': {
                'label': 'State of the participation.'
            }
        }


class EditionFormSerializer(serializers.ModelSerializer):
    """Serializer for edition form objects."""

    edition = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:  # noqa
        model = EditionForm
        fields = ('id', 'edition', 'deadline')


class EditionFormDetailSerializer(EditionFormSerializer):
    """Detail serializer for edition form objects."""

    form = FormDetailSerializer()
    recipient = TutorSerializer()

    class Meta(EditionFormSerializer.Meta):  # noqa
        fields = EditionFormSerializer.Meta.fields + ('form', 'recipient',)


class EditionListSerializer(serializers.HyperlinkedModelSerializer):
    """List serializer for Edition objects."""

    description = MarkdownField()
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    organizers = serializers.SerializerMethodField()
    participations = serializers.SerializerMethodField()
    edition_form = EditionFormSerializer()

    def get_organizers(self, obj: Edition) -> int:
        """Return the number of organizers."""
        return obj.organizers.count()

    def get_participations(self, obj: Edition) -> int:
        """Return the number of participations."""
        return obj.participations.count()

    class Meta:  # noqa
        model = Edition
        fields = ('id', 'url', 'name', 'year', 'project', 'description',
                  'organizers', 'participations', 'edition_form',)
        extra_kwargs = {
            'url': {'view_name': 'api:edition-detail'},
        }


class EditionDetailSerializer(EditionListSerializer):
    """Detail serializer for Edition objects."""

    organizers = UserSerializer(many=True)
    participations = ParticipationSerializer(many=True)
    edition_form = EditionFormDetailSerializer()


class ProjectDetailSerializer(ProjectSerializer):
    """Detail serializer for project objects."""

    editions = EditionListSerializer(many=True)

    class Meta(ProjectSerializer.Meta):  # noqa
        fields = ProjectSerializer.Meta.fields + ('editions',)
