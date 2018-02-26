"""Various file utilities."""

import os
import fnmatch


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
