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
                "date_of_birth": "1996-09-02",
                "phone": "xxxxxxxxxx",
                "address": {
                    "line1": "3 Rue Joliot Curie",
                    "line2": "",
                    "post_code": "91190",
                    "city": "Gif-sur-Yvette",
                    "country": {
                        "code": "FR",
                        "name": "France"
                    }
                },
                "emergency_contact": "urgences@oser-cs.fr",
                "submitted": "2018-04-07T23:07:05.943305+02:00"
            }
        ]

    create:

    ### Date of birth

    Date of birth must be sent in a ISO-compliant format (in Javascript, `Date.toISOString()` can be used for this).

    ### Address

    Address format is the following :

        {
            "line1": "...",
            "line2": "...",
            "post_code": "...",
            "city": "...",
            "country": "..."
        }

    `line2` : optional, default is `""`.

    `country` : optional, default is `"FR"`. Must be given as a
    [country code ](https://en.wikipedia.org/wiki/Country_code).
    """

    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (DRYPermissions,)
