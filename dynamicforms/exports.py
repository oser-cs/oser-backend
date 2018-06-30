"""Data export utilities."""


from typing import List
import os
import zipfile
import csv
from io import BytesIO, StringIO
from .models import Form
from django.db.models.fields.files import FieldFile


def _get_rows(form: Form) -> List[List[str]]:
    """Return CSV rows of form entries, including the header row."""
    rows = []

    sections = form.sections.prefetch_related('questions').all()

    def sections_questions():
        for section in sections:
            for question in section.questions.all():
                yield section, question

    def build_row(entry) -> List[str]:
        row = [entry.submitted.strftime("%Y-%m-%d %H:%M")]
        for _, question in sections_questions():
            answer = entry.answers.filter(question=question).first()
            value: str = answer and (answer.answer or '') or ''
            row.append(value)
        return row

    # Build the header row
    headers = ['Soumis le']
    for section, question in sections_questions():
        headers.append(f'{section.title}: {question.text}')

    rows.append(headers)

    # Add a row for each form entry
    for entry in form.entries.prefetch_related('answers').all():
        row = build_row(entry)
        rows.append(row)

    return rows


def _write_csv(form: Form, stream):
    """Write a form's entries into a stream in CSV format."""
    writer = csv.writer(stream)

    for row in _get_rows(form):
        writer.writerow(row)

    return stream


def write_zip(forms, stream=None, folder='forms'):
    """Write forms' entries into a zip of CSV files."""
    if stream is None:
        stream = BytesIO()
    # See https://stackoverflow.com/a/32075279
    assert not isinstance(stream, StringIO), (
        'cannot write binary zip file contents to a StringIO object, '
        'consider using BytesIO instead'
    )
    with zipfile.ZipFile(stream, 'w') as zip:
        for form in forms:
            csv_file = StringIO()
            _write_csv(form, csv_file)
            csv_filename = os.path.join(folder, f'{form.slug}.csv')
            value = csv_file.getvalue()
            zip.writestr(csv_filename, value.encode())
    return stream


def files_zip(files: List[FieldFile], folder: str='') -> BytesIO:
    """Write form's files into a ZIP."""
    stream = BytesIO()
    with zipfile.ZipFile(stream, 'w') as zip:
        for file in files:
            dest = os.path.join(folder, os.path.basename(file.name))
            contents = file.read()
            zip.writestr(dest, contents)
        # fix for Linux zip files read in Windows
        for file in zip.filelist:
            file.create_system = 0
    stream.seek(0)
    return stream
