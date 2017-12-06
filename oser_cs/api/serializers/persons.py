"""Persons API serializers."""

from rest_framework import serializers
from persons.models import Tutor


class TutorSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Tutor."""

    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='api:user-detail',
    )
    tutoring_groups = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:tutoringgroup-detail',
    )

    class Meta:  # noqa
        model = Tutor
        fields = ('user', 'promotion', 'tutoring_groups',)
        extra_kwargs = {
            'url': {
                'view_name': 'api:tutor-detail',
            }
        }
