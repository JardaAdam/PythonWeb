import re
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError



def validate_no_numbers(value):
    if re.search(r'\d', value):
        raise ValidationError("Jméno nesmí obsahovat čísla.")

def validate_postcode(postcode, country):
    if not postcode:
        raise ValidationError("Poštovní směrovací číslo nesmí být prázdné.")

    # Validate postcode using regex
    if hasattr(country, 'postcode_validator'):
        postcode_validator = RegexValidator(
            regex=country.postcode_validator,
            message=f"Poštovní směrovací číslo neodpovídá formátu pro zvolenou zemi {country.name}. "
                    f"Očekávaný formát je: {country.postcode_format}."
        )
        postcode_validator(postcode)

    return postcode

def validate_phone_number(phone_number, country):
    if not phone_number:
        raise ValidationError("Telefonní číslo je povinné.")

    # Přidejte phone_number_prefix, pokud chybí
    if country.phone_number_prefix and not phone_number.startswith(country.phone_number_prefix):
        phone_number = f"{country.phone_number_prefix}{phone_number}"

    # Validate phone number using regex
    if hasattr(country, 'phone_number_validator'):
        phone_number_validator = RegexValidator(
            regex=country.phone_number_validator,
            message=f"Telefonní číslo neodpovídá formátu pro zvolenou zemi {country.name}."
                    f"Očekávaný formát je: {country.phone_number_format}."
        )
        phone_number_validator(phone_number)

    # Return the potentially updated phone number with prefix
    return phone_number

def validate_business_id(business_id, country):
    if not business_id:
        # Pokud je business_id prázdný, není potřebná žádná validace.
        return business_id

    # Validate business_id format using regex
    if country.business_id_validator:
        business_id_validator = RegexValidator(
            regex=country.business_id_validator,
            message=f"Business ID neodpovídá formátu pro zvolenou zemi {country.name}. "
                    f"Očekávaný formát je: {country.business_id_format}."
        )
        business_id_validator(business_id)

    # Return the potentially updated business_id
    return business_id

def validate_tax_id(tax_id, country):
    if not tax_id:
        # Pokud je tax_id prázdný, není potřebná žádná validace.
        return tax_id

    # Přidejte tax_id_prefix, pokud chybí
    if country.tax_id_prefix and not tax_id.startswith(country.tax_id_prefix):
        tax_id = f"{country.tax_id_prefix}{tax_id}"

    # Validate tax_id using regex
    if hasattr(country, 'tax_id_validator'):
        tax_id_validator = RegexValidator(
            regex=country.tax_id_validator,
            message=f"Tax ID neodpovídá formátu pro zvolenou zemi {country.name}. "
                    f"Očekávaný formát je: {country.tax_id_format}."
        )
        tax_id_validator(tax_id)

    # Return the potentially updated tax_id with prefix
    return tax_id



