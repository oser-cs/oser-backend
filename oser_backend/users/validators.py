"""Users validators."""

from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message=("Veuillez entrer un numéro de téléphone au format international: "
             "+999999999 (jusqu'à 15 numéros acceptés)")
)
