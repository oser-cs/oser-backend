"""AttachedFile model tests."""
from tests.utils import ModelTestCase
from visits.factory import VisitFactory
from visits.models import AttachedFile


class AttachedFileTest(ModelTestCase):
    """Test the AttachedFile model."""

    model = AttachedFile
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
        cls.obj = AttachedFile.objects.create(name='My attached file',
                                                   visit=visit,
                                                   required=True)

    def test_str_is_name(self):
        self.assertEqual(str(self.obj), str(self.obj.name))
