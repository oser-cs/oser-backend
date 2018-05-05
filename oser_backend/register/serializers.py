"""Register serializers."""

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from core.models import Address
from core.serializers import AddressSerializer
from tutoring.models import School, TutoringGroup
from profiles.models import Student

from .models import EmergencyContact, Registration


User = get_user_model()


class EmergencyContactSerializer(serializers.ModelSerializer):
    """Serializer for emergency contacts."""

    class Meta:  # noqa
        model = EmergencyContact
        fields = ('first_name', 'last_name',
                  'email', 'home_phone', 'mobile_phone')


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for documents."""

    password = serializers.CharField(
        help_text='Mot de passe',
        write_only=True,
        style={'input_type': 'password'},
    )
    tutoring_group = serializers.PrimaryKeyRelatedField(
        label='Groupe de tutorat',
        help_text='Identifiant du groupe de tutorat du lycéen',
        queryset=TutoringGroup.objects.all(),
        required=False,
        write_only=True,
    )
    school = serializers.PrimaryKeyRelatedField(
        label='Lycée',
        help_text='Identifiant du lycée du lycéen',
        queryset=School.objects.all(),
        required=False,
        write_only=True,
    )
    address = AddressSerializer(
        required=False,
        help_text="Adresse du lycéen")
    emergency_contact = EmergencyContactSerializer(
        required=False,
        help_text="Contact en cas d'urgence")
    validated = serializers.HiddenField(default=False)

    class Meta:  # noqa
        model = Registration
        fields = ('id', 'email', 'password',
                  'first_name', 'last_name', 'date_of_birth', 'phone',
                  'tutoring_group', 'school',
                  'submitted', 'validated',
                  'address', 'emergency_contact',)

        extra_kwargs = {
            'submitted': {'read_only': True},
        }

    def validate_email(self, email):
        """Check that the email does not refer to an already existing user."""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'User with this email already exists')
        return email

    def validate(self, data):
        """Validate object-level input data.

        Tutoring group and school:
        - If the group is given, check the school is also given
        - The group must belong to the school
        """
        data = super().validate(data)
        tutoring_group = data.get('tutoring_group', None)
        school = data.get('school', None)

        if tutoring_group:
            if not school:
                raise serializers.ValidationError(
                    'tutoring_group is set: expected school too, none given')

            if tutoring_group.school != school:
                raise serializers.ValidationError(
                    'tutoring group must belong to school')

        return data

    def create(self, validated_data):
        """Create the registration from validated data.

        - Build/save the nested objects (address, emergency contact)
        - Build/save a user and a student profile
        """
        password = validated_data.pop('password')
        address_data = validated_data.pop('address', None)
        emergency_contact_data = validated_data.pop('emergency_contact', None)
        tutoring_group = validated_data.pop('tutoring_group', None)
        school = validated_data.pop('school', None)

        # The following block will create a bunch of objects and save them
        # in the database. We don't want them to be saved separately.
        # => Use an atomic transaction to not save anything in case an
        # exception is raised.
        # (Hint: it disables the autocommit mode and commit all queries at
        # the end of the "with" block.)
        # See the Django docs on atomic transactions for more info.
        with transaction.atomic():

            # Create the address if given
            if address_data:
                address = Address.objects.create(**address_data)
            else:
                address = None

            # Create the emergency contact if given
            if emergency_contact_data:
                emergency_contact = EmergencyContact.objects.create(
                    **emergency_contact_data)
            else:
                emergency_contact = None

            # Create the user
            user = User.objects.create_user(
                email=validated_data['email'],
                password=password,
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                date_of_birth=validated_data.get('date_of_birth'),
                phone_number=validated_data.get('phone'),
            )

            # Create the registration
            registration = Registration.objects.create(
                **validated_data,
                address=address,
                emergency_contact=emergency_contact,
            )

            # Create the student profile and tie the registration to it
            Student.objects.create(
                user=user,
                school=school,
                tutoring_group=tutoring_group,
                registration=registration,
            )

        return registration


class StudentRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registration objects, suited to attach to a student."""

    class Meta:
        model = Registration
        fields = ('id', 'submitted', 'validated',)

        extra_kwargs = {
            'submitted': {'read_only': True},
            'validated': {'read_only': True},
        }
