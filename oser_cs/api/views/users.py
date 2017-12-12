"""Users API views."""

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from api.serializers.users import UserSerializer, UserCreateSerializer

# Create your views here.

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited.

    retrieve:
    Return a user instance.

    list:
    Return all users.

    create:
    Create a user instance.
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
