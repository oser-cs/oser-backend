"""Profiles serializers."""

from rest_framework import serializers

from register.serializers import StudentRegistrationSerializer
from users.serializers import UserSerializer

from .models import Student, Tutor


class TutorSerializer(serializers.HyperlinkedModelSerializer):
    """Hyperlinked serializer for Tutor."""

    user = UserSerializer()

    class Meta:  # noqa
        model = Tutor
        fields = ('user', 'promotion', 'url',)
        extra_kwargs = {
            'url': {'view_name': 'api:tutor-detail'},
        }


class StudentSerializer(serializers.ModelSerializer):
    """Hyperlinked serializer for Student."""

    user = UserSerializer()
    visits = serializers.PrimaryKeyRelatedField(
        source='user.visit_set',
        many=True,
        read_only=True)
    registration = StudentRegistrationSerializer()

    class Meta:  # noqa
        model = Student
        fields = (
            'user_id', 'url', 'gender', 'addressNumber', 'street', 'city', 'personnalPhone', 'parentsPhone', 'parentsEmail', 'school', 'grade', 'scholarship', 'fatherActivity', 'motherActivity', 'parentsStatus', 'dependantsNumber')
        extra_kwargs = {
            'url': {'view_name': 'api:student-detail'},
        }
