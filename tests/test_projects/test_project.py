"""Test the Project model."""

from tests.utils import ModelTestCase
from projects.models import Project
from projects.factory import ProjectFactory


class ProjectModelTest(ModelTestCase):
    """Test the Project model."""

    model = Project
    field_tests = {
        'name': {
            'verbose_name': 'nom',
            'max_length': 200,
        },
        'logo': {
            'upload_to': 'projects/logos/',
        },
    }
    model_tests = {
        'verbose_name': 'projet',
        'ordering': ('name',),
    }

    def setUp(self):
        self.project = ProjectFactory.create()

    def test_str_is_name(self):
        self.assertEqual(str(self.project), self.project.name)

    def test_has_editions(self):
        self.assertEqual(0, self.project.editions.count())
