"""Dynamic forms tests."""

from io import StringIO, BytesIO
from django.test import TestCase
from .models import Form, Section, Question, FormEntry, Answer
from .exports import _write_csv, _get_rows, write_zip


class WriteCsvTest(TestCase):
    """Test the CSV export utility."""

    def setUp(self):
        # Create a form
        form = Form.objects.create(title='Animals')

        # Add a section
        section = Section.objects.create(
            form=form,
            title='Dogs')

        # Add two questions in the section
        have_dog = Question.objects.create(
            text='Do you have a dog?',
            type=Question.TYPE_YES_NO,
            section=section)
        Question.objects.create(
            text='If yes, what is its name?',
            type=Question.TYPE_TEXT_SMALL,
            required=False,
            section=section)

        # Create an entry
        entry = FormEntry.objects.create(form=form)
        # Add 1 answer to the entry, leave the other answer blank
        Answer.objects.create(question=have_dog, entry=entry, answer='No')

        self.form = Form.objects.get(pk=form.pk)
        self.entry = FormEntry.objects.get(pk=entry.pk)

    def test_get_rows(self):
        rows = _get_rows(self.form)
        self.assertEqual(len(rows), 2)
        expected_headers = [
            'Soumis le',
            'Dogs: If yes, what is its name?',
            'Dogs: Do you have a dog?',
        ]
        self.assertListEqual(rows[0], expected_headers)
        expected_entry_row = [
            self.entry.submitted.strftime("%Y-%m-%d %H:%M"),
            '',
            'No',
        ]
        self.assertListEqual(rows[1], expected_entry_row)

    def test_write_csv_runs_without_failing(self):
        stream = StringIO()
        _write_csv(self.form, stream)
        stream.seek(0)
        stream.read()

    def test_write_zip_runs_without_failing(self):
        stream = BytesIO()
        write_zip([self.form], stream=stream)
        stream.seek(0)
        stream.read()
