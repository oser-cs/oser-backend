"""Person abstract model tests."""

from django.contrib.auth import get_user_model
from persons.models import Person

from tests.utils import random_email, MixinModelTestCase


User = get_user_model()


class PersonTestCase(MixinModelTestCase):
    """Test case for Person abstract model."""

    mixin = Person
    field_tests = {
        'user': {
            'verbose_name': 'utilisateur',
        },
    }

    @classmethod
    def setUpTestData(self):
        user = User.objects.create(email=random_email())
        self.obj = self.model.objects.create(user=user)

    def test_user_one_to_one_relationship(self):
        self.assertEqual(User.objects.get(), self.obj.user)
