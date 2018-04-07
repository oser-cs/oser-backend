"""Register serializers."""

from rest_framework import serializers

from .models import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for documents."""

    class Meta:  # noqa
        model = Registration
        fields = ('id', 'first_name', 'last_name', 'email', 'phone',
                  'date_of_birth', 'submitted',)
        extra_kwargs = {
            'submitted': {'read_only': True},
        }
