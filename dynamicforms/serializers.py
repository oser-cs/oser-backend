"""Dynamic forms serializers."""

from rest_framework import serializers
from .models import Form, Section, Question, Answer, FormEntry, File


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for form questions."""

    class Meta:  # noqa
        model = Question
        fields = ('id', 'type', 'text', 'help_text', 'required', 'section',)


class SectionSerializer(serializers.ModelSerializer):
    """Serializer for form sections."""

    questions = QuestionSerializer(many=True)

    class Meta:  # noqa
        model = Section
        fields = ('id', 'title', 'questions', 'form')


class FileSerializer(serializers.ModelSerializer):
    """Serializer for form files."""

    class Meta:  # noqa
        model = File
        fields = ('id', 'name', 'file', 'form')


class FormSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for forms."""

    class Meta:  # noqa
        model = Form
        fields = ('id', 'url', 'slug', 'title', 'entries_count',)
        extra_kwargs = {
            'url': {'view_name': 'api:form-detail'},
        }


class FormDetailSerializer(FormSerializer):
    """Serializer for form detail."""

    sections = SectionSerializer(many=True)
    files = FileSerializer(many=True)

    class Meta(FormSerializer.Meta):  # noqa
        fields = FormSerializer.Meta.fields + ('sections', 'files',)


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for submitting answers."""

    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(),
    )

    class Meta:  # noqa
        model = Answer
        fields = ('id', 'question', 'entry', 'answer')
        extra_kwargs = {
            'entry': {'read_only': True},
        }


class FormEntrySerializer(serializers.ModelSerializer):
    """Serializer for creating form entries."""

    form = serializers.PrimaryKeyRelatedField(
        queryset=Form.objects.all(),
    )
    answers = AnswerSerializer(many=True)

    class Meta:  # noqa
        model = FormEntry
        fields = ('id', 'form', 'submitted', 'answers',)
