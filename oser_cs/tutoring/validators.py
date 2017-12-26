"""Tutoring validators."""

from django.core.validators import RegexValidator


uai_code_validator = RegexValidator(
    regex=r'^\d{7}[a-zA-Z]$',
    message=("Un code UAI doit être composé de 7 chiffres "
             "suivis d'une lettre.")
)
