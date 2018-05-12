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
                "date_of_birth": null,
                "phone": null,
                "school": "0930965U",
                "grade": "Première S",
                "submitted": "2018-05-05T14:15:10.998206+02:00",
                "address": {
                    "line1": "88 bis rue Jules Guesde",
                    "line2": "",
                    "post_code": "93100",
                    "city": "Montreuil",
                    "country": {
                        "code": "FR",
                        "name": "France"
                    }
                },
                "emergency_contact": {
                    "first_name": "Marie-Claude",
                    "last_name": "Perret",
                    "email": null,
                    "home_phone": "+33312344556",
                    "mobile_phone": null
                }
            }
        ]

    create:

    This endpoint allows to create a registration for a student.

    In fact, it does three things:

    1. Create a user for the student
    2. Create the registration
    3. Create a student profile and link it to the user and the registration.

    ### Date of birth

    Date of birth must be sent in a ISO-compliant format (in Javascript,
    `Date.toISOString()` can be used for this).

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
    [country code](https://en.wikipedia.org/wiki/Country_code).

    ### Emergency contact

    Emergency contact format is the following:

        {
            "first_name": "...",
            "last_name": "...",
            "email": "...",
            "home_phone": "...",
            "mobile_phone": "..."
        }

    `email` must be a valid email address. Phone format for `home_phone`
    and `mobile_phone` is not verified.

    ### School

    The value given must be the school's `uai_code`.
    You can retrieve the list of available schools thanks to the
    [schools-choices](#schools-choices) endpoint.
    """

    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (DRYPermissions,)
