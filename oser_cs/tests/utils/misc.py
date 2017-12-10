"""Generic test function generators and other test utilities."""

import random
from string import ascii_lowercase, digits


__all__ = ('random_username', 'random_email', 'random_uai_code')


def random_username():
    """Return a random username with 12 lowercase letters."""
    return ''.join(random.choices(ascii_lowercase, k=12))


def random_email():
    """Return a random email."""
    prefix = ''.join(random.choices(ascii_lowercase, k=12))
    return f'{prefix}@random.net'


def random_uai_code():
    """Return a random UAI code (French school identifier)."""
    seven_digits = ''.join(random.choices(digits, k=7))
    one_letter = random.choice(ascii_lowercase)
    return seven_digits + one_letter
