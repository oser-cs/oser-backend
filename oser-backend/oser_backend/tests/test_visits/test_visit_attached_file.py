"""VisitAttachedFile model tests."""
from tests.utils import ModelTestCase
from visits.factory import VisitFactory
from visits.models import VisitAttachedFile


class VisitAttachedFileTest(ModelTestCase):
    """Test the VisitAttachedFile model."""

    model = VisitAttachedFile
    field_tests = {
        'name': {
            'verbose_name': 'nom',
            'max_length': 200,
        },
        'required': {
            'verbose_name': 'requis',
            'default': True,
        },
        'visit': {
            'verbose_name': 'sortie',
        },
    }
    model_tests = {
        'verbose_name': 'pièce jointe',
        'verbose_name_plural': 'pièces jointes',
        'ordering': ('visit',),
    }

    @classmethod
    def setUpTestData(cls):
        visit = VisitFactory.create()
        cls.obj = VisitAttachedFile.objects.create(name='My attached file',
                                                   visit=visit,
                                                   required=True)

    def test_str_is_name(self):
        self.assertEqual(str(self.obj), str(self.obj.name))
