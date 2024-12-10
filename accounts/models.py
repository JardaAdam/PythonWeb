from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def validate_discount(value):
    """Validuje, zda je sleva mezi 0 a 100%."""
    if value < 0 or value > 100:
        raise ValidationError("Sleva musí být mezi 0 a 100%.")

class CustomUser(AbstractUser):
    company_name = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    postcode = models.CharField(
        max_length=6, null=True, blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\s?\d{2}$',  # Formát: 3 číslice + volitelná mezera + 2 číslice
                message="Poštovní směrovací číslo musí mít formát XXX XX (např. 11000 nebo 110 00)."
            )
        ],
        verbose_name="Poštovní směrovací číslo"
    )
    phone_number = models.CharField(
        max_length=17, blank=True, null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Telefonní číslo musí být ve formátu: '+420123456789'. Až 15 číslic je povoleno."
            )
        ],
        help_text="Zadejte telefonní číslo v mezinárodním formátu, např. +420123456789."
    )
    ico = models.CharField(max_length=8, null=True, blank=True)
    dic = models.CharField(max_length=11, null=True, blank=True)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00,
        validators=[validate_discount],
        help_text="Zadejte slevu v procentech (např. 10.5 = 10.5%)."
    )

    class Meta:
        ordering = ['username']

    def __repr__(self):
        return f"CustomUser(username={self.username})"

    def __str__(self):
        return f"{self.username}"