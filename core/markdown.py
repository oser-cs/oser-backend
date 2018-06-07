"""Markdown utilities."""

from typing import Generator as Gen
import re
from pathlib import Path


class MdFileRef:
    """Represents a Markdown file reference."""

    str_format = '[{legend}]({file_path})'
    pattern = r'\[(?P<legend>.*?)\]\((?P<file_path>.*?)\)'

    def __init__(self, legend: str='', file_path: str=''):
        self.legend = legend
        self.file_path = file_path

    @classmethod
    def find(cls, text: str) -> Gen['cls', None, None]:
        """Find all file references in text.

        Returns iterable of MdFileRef objects.
        """
        pattern = re.compile(cls.pattern)
        for match in pattern.finditer(text):
            yield cls(legend=match.group('legend'),
                      file_path=match.group('file_path'))

    @property
    def filename(self) -> str:
        return Path(self.file_path).name

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self)

    def __str__(self):
        return self.str_format.format(legend=self.legend,
                                      file_path=self.file_path)


class MdImageRef(MdFileRef):
    """Represents a Markdown image reference."""

    str_format = '!' + MdFileRef.str_format
    pattern = r'!' + MdFileRef.pattern


def extract_md_file_refs(markdown_text: str) -> Gen[MdImageRef, None, None]:
    """Return iterator of file (and image) references in markdown text."""
    for ref in MdFileRef.find(markdown_text):
        yield ref


def extract_image_refs(markdown_text: str) -> Gen[MdImageRef, None, None]:
    """Return iterator of image references in markdown text."""
    for ref in MdImageRef.find(markdown_text):
        yield ref


def _get_domain(request):
    schema = 'https://' if request.is_secure() else 'http://'
    return schema + request.get_host()


def add_domain_to_image_files(request, content: str) -> str:
    """Add domain to image file path in image references.

    This allows to get full URL to image inside ![]() tags,
    and allows a foreign server that has access to the backend server
    to render them directly.
    """
    domain = _get_domain(request)
    for ref in MdImageRef.find(content):
        # skip links to external images
        if ref.file_path.startswith('http'):
            continue
        new_ref = MdImageRef(legend=ref.legend,
                             file_path=domain + ref.file_path)
        content = content.replace(str(ref), str(new_ref))
    return content
