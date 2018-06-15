"""Dynamic forms utilities."""

import os


def file_upload_to(instance: 'File', filename: str) -> str:
    """Return the upload path to a form file."""
    return os.path.join('forms', 'files', instance.form.title, filename)
