import os.path
from django.test import TestCase
from django.core.files.storage import default_storage
from django.core.files import File
from django.core.management import call_command
from visits.factory import VisitFactory
from visits.models import Visit
from core.management.commands.utils import DataLoader


class CleanMediaTest(TestCase):
    """Test the cleanmedia command."""

    ref_file_name = 'visit-factsheet.pdf'
    safe_location = 'you_will_not_find_me'
    non_ref_file_name = 'example.txt'
    non_ref_file_path = os.path.join(safe_location, non_ref_file_name)

    def setUp(self):
        # create objects in DB with references to files
        with DataLoader().load(self.ref_file_name) as fact_sheet:
            visit = VisitFactory.create(fact_sheet=fact_sheet)
            self.ref_file = visit.fact_sheet  # FieldFile object
        # add files that are not referenced in DB
        with DataLoader().load(self.non_ref_file_name) as example_file:
            self.non_ref_file = File(example_file)
            default_storage.save(self.non_ref_file_path, self.non_ref_file)

    def test_command(self):
        """Call the command to check no error occurs."""
        ref_file_dir = Visit._meta.get_field('fact_sheet').upload_to
        ref_file_path = os.path.join(ref_file_dir, self.ref_file_name)

        # check that files are well in the storage
        self.assertTrue(default_storage.exists(ref_file_path))
        self.assertTrue(default_storage.exists(self.non_ref_file_path))

        # call the command
        call_command('cleanmedia', top=self.safe_location, verbosity=0)

        # file under test_files/ without reference must have been deleted
        self.assertFalse(default_storage.exists(self.non_ref_file_path))
        # file with ref in DB must not have been deleted
        self.assertTrue(default_storage.exists(ref_file_path))

        # safe location must have been emptied and deleted
        self.assertFalse(default_storage.exists(self.safe_location))
