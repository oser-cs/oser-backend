"""Profiles serializers."""

from rest_framework import serializers

from core.serializers import AddressSerializer
from register.serializers import (EmergencyContactSerializer,
                                  StudentRegistrationSerializer)
from tutoring.models import School, TutoringGroup
from users.serializers import UserSerializer

from .models import Student, Tutor


class TutorSerializer(serializers.HyperlinkedModelSerializer):
    """Hyperlinked serializer for Tutor."""

    user = UserSerializer()
    tutoring_groups = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    address = AddressSerializer()

    class Meta:  # noqa
        model = Tutor
        fields = ('user', 'address', 'promotion', 'tutoring_groups', 'url',)
        extra_kwargs = {
            'url': {'view_name': 'api:tutor-detail'},
        }


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    """Hyperlinked serializer for Student."""

    user = UserSerializer()
    tutoring_group = serializers.PrimaryKeyRelatedField(
        queryset=TutoringGroup.objects.all(),
    )
    school = serializers.PrimaryKeyRelatedField(
        queryset=School.objects.all(),
    )
    visits = serializers.PrimaryKeyRelatedField(
        source='user.visit_set',
        many=True,
        read_only=True)
    address = AddressSerializer()
    emergency_contact = EmergencyContactSerializer()
    registration = StudentRegistrationSerializer()

    class Meta:  # noqa
        model = Student
        fields = ('user_id', 'user', 'address', 'tutoring_group',
                  'school', 'emergency_contact', 'registration',
                  'visits', 'url',)
        extra_kwargs = {
            'url': {'view_name': 'api:student-detail'},
        }
