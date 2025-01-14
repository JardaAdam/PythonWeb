from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def validate_business_id(business_id, country):
    if country.business_id_validator:
        business_id_validator = RegexValidator(
            regex=country.business_id_validator,
            message=f"Business ID neodpovídá formátu pro zvolenou zemi {country.name}."
                    f"Očekávaný formát je: {country.business_id_format}."
        )
        business_id_validator(business_id)
# TODO zajistit aby funkce kontrolovala delku tax_id, pridavala CZ prefix pokud neni vyplnen
def validate_tax_id(tax_id, country):
    if country.tax_id_validator:
        tax_id_validator = RegexValidator(
            regex=country.tax_id_validator,
            message=f"Tax ID neodpovídá formátu pro zvolenou zemi {country.name}."
                    f"Očekávaný formát je: {country.tax_id_format}."
        )
        tax_id_validator(tax_id)
# todo udelat validacny funkci pro cislo
def validate_phone_number(phone_number, country):
    if phone_number and country.phone_number_prefix:
        if not phone_number.startswith(country.phone_number_prefix):
            return f"{country.phone_number_prefix}{phone_number}"
    return phone_number

def validate_postcode(postcode, country):
    if country.postcode_validator:
        postcode_validator = RegexValidator(
            regex=country.postcode_validator,
            message=f"Poštovní směrovací číslo neodpovídá formátu pro zvolenou zemi {country.name}."
                    f"Očekávaný formát je: {country.postcode_format}."
        )
        postcode_validator(postcode)