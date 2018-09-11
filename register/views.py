"""Register views."""

from dry_rest_permissions.generics import DRYPermissions
from rest_framework import mixins, viewsets

from .models import Registration
from .serializers import RegistrationSerializer


# Create your views here.


class RegistrationViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """API endpoints to create and list registrations.

    list:

    ### Example response

        [
            {
                "id": 3,
                "email": "charles.dumont@example.net",
                "first_name": "Charles",
                "last_name": "Dumont",
                "submitted": "2018-05-05T14:15:10.998206+02:00",
            }
        ]

    create:

    This endpoint allows to create a registration for a student.

    In fact, it does three things:

    1. Create a user for the student
    2. Create the registration
    3. Create a student profile and link it to the user and the registration.
    """

    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (DRYPermissions,)
