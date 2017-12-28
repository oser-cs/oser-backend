"""Tutoring utilities."""

import random
from string import ascii_lowercase, digits


def random_uai_code():
    """Return a random UAI code (French school identifier)."""
    seven_digits = ''.join(random.choices(digits, k=7))
    one_letter = random.choice(ascii_lowercase)
    return seven_digits + one_letter
