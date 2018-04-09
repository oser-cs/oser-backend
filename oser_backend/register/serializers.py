"""Register serializers."""

from rest_framework import serializers
from .models import Registration
from core.serializers import AddressSerializer
from core.models import Address


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for documents."""

    address = AddressSerializer(
        required=False,
        help_text="Adresse du lycéen")

    class Meta:  # noqa
        model = Registration
        fields = ('id', 'first_name', 'last_name', 'date_of_birth',
                  'email', 'phone', 'address', 'emergency_contact',
                  'submitted',)
        extra_kwargs = {
            'submitted': {'read_only': True},
        }

    def create(self, validated_data):
        """Override for writable nested address field."""
        address_data: dict = validated_data.pop('address', None)

        registration = Registration.objects.create(**validated_data)

        if address_data:
            address = Address.objects.create(**address_data)
            registration.address = address
            registration.save()

        return registration
