from django.contrib.auth.models import User
from django.db.models import Model, OneToOneField, CASCADE, CharField, DecimalField

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_discount(value):
    """Validuje, zda je sleva mezi 0 a 100%."""
    if value < 0 or value > 100:
        raise ValidationError("Sleva musí být mezi 0 a 100%.")


# # TODO použití AbstractUser pro základní funkcionalitu a
# #  Profile použít jen pro položky které nejsou v User
# # Create your models here.
class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    company_name = CharField(max_length=32, null=True, blank=True)
    address = CharField(max_length=128, null=True, blank=True)
    city = CharField(max_length=32, null=True, blank=True)
    postcode = CharField(max_length=6, null=True, blank=True,validators=[
            RegexValidator(
                regex=r'^\d{3}\s?\d{2}$',  # Formát: 3 číslice + volitelná mezera + 2 číslice
                message="Poštovní směrovací číslo musí mít formát XXX XX (např. 11000 nebo 110 00)."
            )
        ],verbose_name="Poštovní směrovací číslo")
    # předvolby = foreingkey
    phone_number = CharField(
        max_length=17,  # +420123456789 = 13 znaků, ale ponechte rezervu
        blank=True,
        null=True,
        validators=[RegexValidator(
                        regex=r'^\+?1?\d{9,15}$',
                        message="Telefonní číslo musí být ve formátu: '+420123456789'. Až 15 číslic je povoleno.")],
        help_text="Zadejte telefonní číslo v mezinárodním formátu, např. +420123456789."
    )
    # TODO přepsat do malích písmen !!
    ICO = CharField(max_length=8, null=True, blank=True)
    DIC = CharField(max_length=11, null=True, blank=True)
    discount = DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[validate_discount],
        help_text="Zadejte slevu v procentech (např. 10.5 = 10.5%)."
    )

    class Meta:
        ordering = ['user__username']

    def __repr__(self):
        return f"Profile(user={self.user})"

    def __str__(self):
        return f"{self.user}"



    # TODO doresit odkud se budou brat Jméno, přijmení, email,

