"""Various file utilities."""

import os
import re
import fnmatch
import pathlib


def locate(pattern, root=os.curdir):
    """Locate all files matching pattern in and below given root directory."""
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)


def find_file(pattern, root=os.curdir):
    """Return first occurence of matching file in and below root.

    If no occurence file, raises a FileNotFoundError.
    """
    for path in locate(pattern, root=root):
        return path
    raise FileNotFoundError(pattern)


def extract_md_file_refs(markdown_text):
    """Return iterator of file references in markdown text.

    References come in two forms:
    - image references : ![<legend>](<file_path>)
    - other references : [<legend>](<file_path>)

    Only the filename of each file reference is returned, not the full
    file path.

    The file path is not guaranteed to be an existing file.
    In particular, it may be a web URL instead of a file path.
    => The caller needs to validate the returned references.

    Example
    -------
    list(extract_md_file_refs('[](path/to/hello.png)')) => ['hello.png']
    """
    pattern = re.compile(r'\[(?P<legend>.*?)\]\((?P<file_path>.*?)\)')
    for match in pattern.finditer(markdown_text):
        path = pathlib.Path(match.group('file_path'))
        # only yield the filename, not the entire file path
        yield path.name
