"""Generic test function generators and other test utilities."""

import random
from string import ascii_lowercase


def random_username():
    """Return a random username with 12 lowercase letters."""
    return ''.join(random.choices(ascii_lowercase, k=12))


def random_email():
    """Return a random email."""
    prefix = ''.join(random.choices(ascii_lowercase, k=12))
    return f'{prefix}@random.net'
