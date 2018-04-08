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
                "id": 1,
                "first_name": "Florimond",
                "last_name": "Manca",
                "email": "florimond.manca@student.ecp.fr",
                "phone": null,
                "date_of_birth": "1996-09-02",
                "submitted": "2018-04-07T23:07:05.943305+02:00"
            }
        ]

    create:

    ### Additional fields information

    Date of birth must be sent in a ISO-compliant format (in Javascript, `Date.toISOString()` can be used for this).

    ### Authentication

    Required for this action.
    """

    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (DRYPermissions,)
