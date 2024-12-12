from django.contrib.auth.models import AbstractUser
from django.db.models import DecimalField, CharField, BooleanField, Model, ManyToManyField, ForeignKey, CASCADE, \
    SET_NULL, DateTimeField

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from revisions.models import RevisionRecord

#TODO related_name kde bude potreba pro funkce
#TODO related_query_name kde bude potreba
def validate_discount(value):
    """Validuje, zda je sleva mezi 0 a 100%."""
    if value < 0 or value > 100:
        raise ValidationError("Sleva musí být mezi 0 a 100%.")

class Country(Model):
    name = CharField(max_length=32, unique=True)
    postcode_format = CharField(max_length=6, blank=True, help_text="Regex pro validaci poštovního směrovacího čísla")
    phone_number_prefix = CharField(max_length=10, blank=True, help_text="Telefonní předvolba")
    business_id_format = CharField(max_length=10, blank=True)  # Regex pro validaci business ID
    tax_id_format = CharField(max_length=12, blank=True)  # Regex pro validaci tax ID
    tax_id_prefix = CharField(max_length=4, blank=True, help_text="Tax ID prefix (např. CZ)")

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    company_name = CharField(max_length=32, null=True, blank=True)
    country = ForeignKey(Country, null=True, blank=True, on_delete=SET_NULL)
    address = CharField(max_length=128, null=True, blank=True)
    city = CharField(max_length=32, null=True, blank=True)
    postcode = CharField(max_length=6, null=True, blank=True)
    phone_number = CharField(max_length=12, blank=True, null=True)
    business_id = CharField(max_length=10, null=True, blank=True, verbose_name="Business ID")
    tax_id = CharField(max_length=12, null=True, blank=True, verbose_name="Tax ID")
    discount = DecimalField(
        max_digits=5, decimal_places=2, default=0.00,
        validators=[validate_discount],
        help_text="Zadejte slevu v procentech (např. 10.5 = 10.5%)."
    )
    can_view_multiple_groups = BooleanField(default=False)  # Extra pole pro přístup

    class Meta:
        ordering = ['username']

    def clean(self):
        super().clean()

        # Validace dle vybrané země
        if self.country:
            if self.country.business_id_format:
                business_id_validator = RegexValidator(
                    regex=self.country.business_id_format,
                    message=f"Business ID neodpovídá formátu pro zvolenou zemi {self.country.name}."
                )
                business_id_validator(self.business_id)

            if self.country.tax_id_format:
                tax_id_validator = RegexValidator(
                    regex=self.country.tax_id_format,
                    message=f"Tax ID neodpovídá formátu pro zvolenou zemi {self.country.name}."
                )
                tax_id_validator(self.tax_id)

            if self.country.phone_number_prefix:
                if self.phone_number is not None and not self.phone_number.startswith(self.country.phone_number_prefix):
                    self.phone_number = f"{self.country.phone_number_prefix}{self.phone_number}"

            if self.country.postcode_format:
                postcode_validator = RegexValidator(
                    regex=self.country.postcode_format,
                    message=f"Poštovní směrovací číslo neodpovídá formátu pro zvolenou zemi {self.country.name}."
                )
                postcode_validator(self.postcode)



    def __repr__(self):
        return f"CustomUser(username={self.username}, country={self.country})"

    def __str__(self):
        return self.username



class ItemGroup(Model):
    name = CharField(max_length=64)
    # TODO lepsi by mohlo bit vypsani firmi pod kterou spada skupina, pro jednotlivce ?
    user = ForeignKey(CustomUser, on_delete=SET_NULL, null=True)
    items = ManyToManyField(RevisionRecord, blank=True)  # Prázdné povolené pro flexibilitu
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} skupina uživatele {self.user.username}"