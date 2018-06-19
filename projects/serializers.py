"""Projects serializers."""

from django.db import transaction
from rest_framework import serializers

from core.fields import MarkdownField
from dynamicforms.serializers import FormDetailSerializer, FormEntrySerializer
from profiles.serializers import TutorSerializer
from users.fields import UserField
from users.serializers import UserSerializer

from .models import Edition, EditionForm, Participation, Project


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Project objects."""

    description = MarkdownField()

    class Meta:  # noqa
        model = Project
        fields = ('id', 'url', 'name', 'description', 'logo')
        extra_kwargs = {
            'url': {'view_name': 'api:project-detail'},
        }


class EditionFormSerializer(serializers.ModelSerializer):
    """Serializer for edition form objects."""

    edition = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.SerializerMethodField()

    def get_title(self, obj) -> str:
        """Return the form's title if form is set."""
        form = getattr(obj, 'form', None)
        return form and str(form) or None

    class Meta:  # noqa
        model = EditionForm
        fields = ('id', 'title', 'edition', 'deadline')


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
    participates = serializers.SerializerMethodField()

    def get_organizers(self, obj: Edition) -> int:
        """Return the number of organizers."""
        return obj.organizers.count()

    def get_participations(self, obj: Edition) -> int:
        """Return the number of participations."""
        return obj.participations.count()

    def get_participates(self, obj: Edition) -> bool:
        """Return whether the current user participates in the edition."""
        request = self.context['request']
        if not request.user:
            return False
        return request.user.pk in obj.participations.values_list('user__pk')

    class Meta:  # noqa
        model = Edition
        fields = ('id', 'url', 'name', 'year', 'project', 'description',
                  'organizers', 'participations', 'edition_form',
                  'participates',)
        extra_kwargs = {
            'url': {'view_name': 'api:edition-detail'},
        }


class ParticipationSerializer(serializers.ModelSerializer):
    """Serializer for project edition participations."""

    user = UserField(
        label='Utilisateur',
        help_text='Identifier for the user who participates.')

    edition_id = serializers.PrimaryKeyRelatedField(
        source='edition',
        queryset=Edition.objects.all(),
        label='Édition',
        help_text='Identifier for the associated edition.')

    edition_form_title = serializers.SerializerMethodField()

    entry = FormEntrySerializer(write_only=True)

    def get_edition_form_title(self, obj: Participation) -> str:
        form = getattr(obj.edition, 'edition_form', None)
        return form and str(form) or None

    def create(self, validated_data: dict) -> Participation:
        """Explicitly create as entry is a nested serializer."""
        with transaction.atomic():
            entry_data = validated_data['entry']
            entry = FormEntrySerializer().create(entry_data)

            participation = Participation.objects.create(
                user=validated_data['user'],
                edition=validated_data['edition'],
                state=Participation.STATE_PENDING,
                entry=entry,
            )

        return participation

    class Meta:  # noqa
        model = Participation
        fields = ('id', 'submitted', 'user',
                  'edition_id', 'edition_form_title',
                  'state', 'entry',)
        extra_kwargs = {
            'state': {
                'label': 'State of the participation.'
            }
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
