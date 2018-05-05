"""Register serializers."""

from rest_framework import serializers

from core.models import Address
from core.serializers import AddressSerializer

from .models import EmergencyContact, Registration


class EmergencyContactSerializer(serializers.ModelSerializer):
    """Serializer for emergency contacts."""

    class Meta:  # noqa
        model = EmergencyContact
        fields = ('first_name', 'last_name',
                  'email', 'home_phone', 'mobile_phone')


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for documents."""

    address = AddressSerializer(
        required=False,
        help_text="Adresse du lycéen")
    emergency_contact = EmergencyContactSerializer(
        required=False,
        help_text="Contact en cas d'urgence")

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
        address_data = validated_data.pop('address', None)
        emergency_contact_data = validated_data.pop('emergency_contact', None)

        registration = Registration.objects.create(**validated_data)

        if address_data:
            address = Address.objects.create(**address_data)
            registration.address = address
            registration.save()

        if emergency_contact_data:
            emergency_contact = EmergencyContact.objects.create(
                **emergency_contact_data)
            registration.emergency_contact = emergency_contact
            registration.save()

        return registration
