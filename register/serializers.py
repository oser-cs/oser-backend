"""Register serializers."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Registration
from .signals import registration_created


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for documents."""

    password = serializers.CharField(
        help_text='Mot de passe',
        write_only=True,
        style={'input_type': 'password'},
    )
    validated = serializers.HiddenField(default=False)

    class Meta:  # noqa
        model = Registration
        fields = ('id', 'email', 'password',
                  'first_name', 'last_name', 'phone_number',
                  'submitted', 'validated',)

        extra_kwargs = {
            'submitted': {'read_only': True},
        }

    def validate_email(self, email):
        """Check that the email does not refer to an already existing user."""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'User with this email already exists')
        return email

    def create(self, validated_data):
        """Create the registration from validated data.

        - Build/save the nested objects (address, emergency contact)
        - Build/save a user and a student profile
        """
        password = validated_data.pop('password')

        registration = Registration.objects.create(**validated_data)

        # Fire a registration_created signal
        registration_created.send(
            sender=Registration,
            instance=registration,
            password=password,
        )

        return registration


class StudentRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registration objects, suited to attach to a student."""

    class Meta:  # noqa
        model = Registration
        fields = ('id', 'submitted', 'validated',)

        extra_kwargs = {
            'submitted': {'read_only': True},
            'validated': {'read_only': True},
        }
