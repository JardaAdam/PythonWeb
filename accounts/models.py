import os
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import CharField, Model, ForeignKey, SET_NULL, DateTimeField, UniqueConstraint, ImageField, \
    BooleanField, EmailField

from django.conf import settings
from .validators import (
    validate_business_id,
    validate_tax_id,
    validate_phone_number,
    validate_postcode,
)

# TODO tabulka ktera bude obsahovat informace o zmenach v jednotlivych zaznamech v databazi

class Country(Model):
    """ Facilitates easier user registration by setting format for individual fields """
    name = CharField(max_length=32, unique=True)
    language_code = CharField(max_length=10, blank=True, help_text="Language code for the user (e.g., 'cs' for Czech)")
    postcode_validator = CharField(max_length=20, blank=True, help_text="Regex for postal code validation")
    postcode_format = CharField(max_length=20, blank=True, help_text="Auxiliary format for postal code")
    phone_number_prefix = CharField(max_length=10, blank=True, help_text="Phone number prefix")
    phone_number_validator = CharField(max_length=20, blank=True, help_text="Regex for phone number validation")
    phone_number_format = CharField(max_length=20, blank=True, help_text="Auxiliary format for phone number")
    business_id_validator = CharField(max_length=20, blank=True, help_text="Regex for business ID validation")
    business_id_format = CharField(max_length=20, blank=True, help_text="Auxiliary format for business ID")
    tax_id_prefix = CharField(max_length=20, blank=True, help_text="Tax ID prefix (e.g., CZ)")
    tax_id_validator = CharField(max_length=20, blank=True, help_text="Regex for tax ID validation")
    tax_id_format = CharField(max_length=20, blank=True, help_text="Auxiliary format for tax ID")

    class Meta:
        ordering = ['name']
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Country(name={self.name})"


class Company(Model):
    # TODO  Created_by, Updated_by uvidi Users CompanySupervisor kteří můžou tento zaznam menit
    # TODO doplnit Email?
    """ Sdruzuje CastomUsers zamestnance do skupiny podle Company"""
    logo = ImageField(upload_to="media/company/", null=True, blank=True)
    name = CharField(max_length=255, unique=True, blank=True, null=True)
    country = ForeignKey(Country, null=True, blank=True, on_delete=SET_NULL, related_name='user_by_country')
    address = CharField(max_length=255, null=True, blank=True)
    city = CharField(max_length=32, null=True, blank=True)
    postcode = CharField(max_length=6, null=True, blank=True)
    phone_number = CharField(max_length=20, null=True, blank=True)
    company_email = EmailField(max_length=254, null=True, blank=True)
    business_id = CharField(max_length=10, null=True, blank=True, verbose_name="Business ID")
    tax_id = CharField(max_length=12, null=True, blank=True, verbose_name="Tax ID")
    created_by = ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=SET_NULL, related_name='created_companies')
    date_joined = DateTimeField(auto_now_add=True)
    updated_by = ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=SET_NULL, related_name='updated_companies')
    last_updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name if self.name else 'Unknown company'

    def __repr__(self):
        return f"Company(name={self.name}, country={self.country})"

    def clean(self):
        super().clean()
        if self.country:
            validate_business_id(self.business_id, self.country)
            validate_tax_id(self.tax_id, self.country)
            validate_phone_number(self.phone_number, self.country)
            validate_postcode(self.postcode, self.country)

    def delete(self, *args, **kwargs):
        # Delete associated files if they exist
        if self.logo and os.path.isfile(self.logo.path):
            os.remove(self.logo.path)

        super().delete(*args, **kwargs)


class CustomUser(AbstractUser):
    photo = ImageField(upload_to="media/user/", null=True, blank=True)
    company = ForeignKey(Company, null=True, blank=True, on_delete=SET_NULL, related_name='company_users')
    country = ForeignKey(Country, null=True, blank=True, on_delete=SET_NULL, related_name='country_users')
    address = CharField(max_length=128, null=True, blank=True)
    city = CharField(max_length=32, null=True, blank=True)
    postcode = CharField(max_length=6, null=True, blank=True)
    phone_number = CharField(max_length=20, blank=True, null=True)
    business_id = CharField(max_length=10, null=True, blank=True, verbose_name="Business ID")
    tax_id = CharField(max_length=12, null=True, blank=True, verbose_name="Tax ID")
    created_by = ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=SET_NULL, related_name='created_users')
    last_updated = DateTimeField(auto_now=True)
    updated_by = ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=SET_NULL, related_name='updated_users')
    is_verified = BooleanField(default=False) # controla zda byl uzivatel zkontrolovan po registraci

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"CustomUser(username={self.username}, company={self.company}, country={self.country})"

    def clean(self):
        super().clean()

        if self.country:
            validate_postcode(self.postcode, self.country)
            validate_phone_number(self.phone_number, self.country)
            validate_business_id(self.business_id, self.country)
            validate_tax_id(self.tax_id, self.country)




class ItemGroup(Model):
    """ zdruzuje polozky z revision/models.py - RevisionRecord do skupiny
    diky tomu muze mit jeden
        - CustomUser rozdelene polozky do vice skupin podle pouziti (rescue bag, working at heihgt equipments
        - Company rozdelene polozky dle zamestnancu/pracovist/aut/atd."""
    photo = ImageField(upload_to="media/item_group/", null=True, blank=True)
    name = CharField(max_length=64)
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, related_name='user_item_groups')
    company = ForeignKey(Company, null=True, blank=True, on_delete=SET_NULL, related_name='company_item_groups')
    created_by = ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=SET_NULL, related_name='created_item_groups')
    created = DateTimeField(auto_now_add=True)
    updated_by = ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=SET_NULL, related_name='updated_item_groups')
    updated = DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'user', 'company'], name='unique_name_user_company')
        ]

    # TODO mozna upravit styl zobrazovani pro vypis v update ItemGroup
    def __str__(self):
        user_name = f"{self.user.first_name} {self.user.last_name}" if self.user else "unknown user"
        company_name = self.company.name if self.company else "unknown company"
        return f"{self.name} Company: {company_name} User: {user_name}"

    def __repr__(self):
        return f"ItemGroup(name={self.name}, user={self.user}, company={self.company})"

    def clean(self):
        if not self.user and not self.company:
            raise ValidationError('At least one of the user or company fields must be filled in.')

    # TODO pridat def uprate pro vymazavani souboru ktere byli prepsany

    def delete(self, *args, **kwargs):

        if self.photo and os.path.isfile(self.photo.path):
            os.remove(self.photo.path)


        # Call the delete function of the parent class
        super().delete(*args, **kwargs)
