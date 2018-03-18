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


def walk(storage, top='/', topdown=True, onerror=None):
    """Implement os.walk using a Django storage.

    Refer to the documentation of os.walk().

    Inspired by: https://gist.github.com/btimby/2175107

    Parameters
    ----------
    storage : django.Storage
    top : str, optional
        Same role as in os.walk().
        The path at which the walk should begin. Root directory by default.
    topdown : bool, optional
        Same role and default value as in os.walk().
    onerror : function, optional
        Same role and default value as in os.walk().
    """
    try:
        dirs, nondirs = storage.listdir(top)
    except (os.error, Exception) as err:
        if onerror is not None:
            onerror(err)
        return

    if topdown:
        yield top, dirs, nondirs
    for name in dirs:
        new_path = os.path.join(top, name)
        # recursively list subdirectories
        for top_, dirs_, nondirs_ in walk(storage, top=new_path):
            yield top_, dirs_, nondirs_
    if not topdown:
        yield top, dirs, nondirs
