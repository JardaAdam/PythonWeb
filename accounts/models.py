from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import CharField, Model, ForeignKey, SET_NULL, DateTimeField, UniqueConstraint

from django.core.validators import RegexValidator





class Country(Model):
    """ Slouzi k jednodussi registraci uzivatele a nastavuje format jednotlivich kolonek"""
    name = CharField(max_length=32, unique=True)
    language_code = CharField(max_length=10, blank=True, help_text="Kód jazyka pro uživatele (např. 'cs' pro češtinu)")
    postcode_format = CharField(max_length=6, blank=True, help_text="Regex pro validaci poštovního směrovacího čísla")
    phone_number_prefix = CharField(max_length=10, blank=True, help_text="Telefonní předvolba")
    business_id_format = CharField(max_length=10, blank=True)  # Regex pro validaci business ID
    tax_id_format = CharField(max_length=12, blank=True)  # Regex pro validaci tax ID
    tax_id_prefix = CharField(max_length=4, blank=True, help_text="Tax ID prefix (např. CZ)")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Country(name={self.name})"

class Company(Model):
    """ Sdruzuje CastomUsers zamestnance do skupiny podle Company"""
    name = CharField(max_length=255, unique=True)
    country = ForeignKey(Country, null=True, blank=True, on_delete=SET_NULL, related_name='companies')
    address = CharField(max_length=255, null=True, blank=True)
    city = CharField(max_length=32, null=True, blank=True)
    postcode = CharField(max_length=6, null=True, blank=True)
    phone_number = CharField(max_length=20, null=True, blank=True)
    business_id = CharField(max_length=10, null=True, blank=True, verbose_name="Business ID")
    tax_id = CharField(max_length=12, null=True, blank=True, verbose_name="Tax ID")
    date_joined = DateTimeField(auto_now_add=True)
    last_updated = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Company(name={self.name}, country={self.country})"

    def clean(self):
        super().clean()
        # Validace dle vybrané země
        if self.country:
            if self.country.business_id_format:
                business_id_validator = RegexValidator(
                    regex=self.country.business_id_format,
                    message=f"Business ID neodpovídá formátu pro zvolenou zemi {self.country.name}. Zkontrolujte formát."
                )
                business_id_validator(self.business_id)

            if self.country.tax_id_format:
                tax_id_validator = RegexValidator(
                    regex=self.country.tax_id_format,
                    message=f"Tax ID neodpovídá formátu pro zvolenou zemi {self.country.name}. Zkontrolujte formát."
                )
                tax_id_validator(self.tax_id)

            if self.country.phone_number_prefix:
                if self.phone_number and not self.phone_number.startswith(self.country.phone_number_prefix):
                    self.phone_number = f"{self.country.phone_number_prefix}{self.phone_number}"

            if self.country.postcode_format:
                postcode_validator = RegexValidator(
                    regex=self.country.postcode_format,
                    message=f"Poštovní směrovací číslo neodpovídá formátu pro zvolenou zemi {self.country.name}."
                )
                postcode_validator(self.postcode)

class CustomUser(AbstractUser):
    company = ForeignKey(Company, null=True, blank=True, on_delete=SET_NULL, related_name='company_users')
    country = ForeignKey(Country, null=True, blank=True, on_delete=SET_NULL,related_name='country_users')
    address = CharField(max_length=128, null=True, blank=True)
    city = CharField(max_length=32, null=True, blank=True)
    postcode = CharField(max_length=6, null=True, blank=True)
    phone_number = CharField(max_length=12, blank=True, null=True)
    business_id = CharField(max_length=10, null=True, blank=True, verbose_name="Business ID")
    tax_id = CharField(max_length=12, null=True, blank=True, verbose_name="Tax ID")
    last_updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"CustomUser(username={self.username}, company={self.company}, country={self.country})"



    def clean(self):
        super().clean()

        # Validace dle vybrané země
        if self.country:
            if self.country.business_id_format:
                business_id_validator = RegexValidator(
                    regex=self.country.business_id_format,
                    message=f"Business ID neodpovídá formátu pro zvolenou zemi {self.country.name}. Zkontrolujte formát."
                )
                business_id_validator(self.business_id)

            if self.country.tax_id_format:
                tax_id_validator = RegexValidator(
                    regex=self.country.tax_id_format,
                    message=f"Tax ID neodpovídá formátu pro zvolenou zemi {self.country.name}. Zkontrolujte formát."
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






class ItemGroup(Model):
    """ zdruzuje polozky z revision/models.py - RevisionRecord do skupiny
    diky tomu muze mit jeden
        - CustomUser rozdelene polozky do vice skupin podle pouziti (rescue bag, working at heihgt equipments
        - Company rozdelene polozky dle zamestnancu/pracovist/aut/atd."""
    name = CharField(max_length=64)
    user = ForeignKey(CustomUser, on_delete=SET_NULL, null=True, related_name='user_item_groups')
    company = ForeignKey(Company, null=True, blank=True, on_delete=SET_NULL, related_name='company_item_groups')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'user', 'company'], name='unique_name_user_company')
        ]

    def clean(self):
        # Zajištění, že je vyplněno alespoň jedno z polí `user` nebo `company`
        if not self.user and not self.company:
            raise ValidationError('Alespoň jedno z pole user nebo company musí být vyplněné.')

    def __str__(self):
        user_name = f"{self.user.first_name} {self.user.last_name}" if self.user else "Žádný uživatel"
        company_name = self.company.name if self.company else "Žádná společnost"
        return f"Revize {self.name} Company: {company_name} User: {user_name}"

    def __repr__(self):
        return f"ItemGroup(name={self.name}, user={self.user}, company={self.company})"