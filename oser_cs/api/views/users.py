"""Users API views."""

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin,
)
from api.serializers.users import UserSerializer

# Create your views here.

User = get_user_model()


class UserViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  CreateModelMixin,
                  viewsets.GenericViewSet):
    """API endpoint that allows users to be viewed or edited.

    retrieve:
    Return a user instance.

    list:
    Return all users.

    create:
    Create a user instance.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
