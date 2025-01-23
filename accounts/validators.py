import re
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def validate_no_numbers(value):
    if re.search(r'\d', value):
        raise ValidationError("The name must not contain numbers.")


def validate_address(address):
    """Validate that the address contains both a street name and a house number,
       and ensure the first letter of each word is capitalized."""
    if not address:
        raise ValidationError("Address is required.")

    # Zkontrolovat, zda adresa obsahuje číslo popisné
    if not re.search(r'\b\d+\b', address):
        raise ValidationError("Address must contain a street name and a house number.")

    # Zvětšit první písmena každého slova
    address = address.strip().capitalize()

    return address

def validate_postcode(postcode, country):
    if not postcode:
        raise ValidationError("Postcode must not be empty.")

    # Validate postcode using regex
    if hasattr(country, 'postcode_validator'):
        postcode_validator = RegexValidator(
            regex=country.postcode_validator,
            message=f"The postcode does not match the format for the selected country {country.name}. "
                    f"Expected format is: {country.postcode_format}."
        )
        postcode_validator(postcode)
    return postcode

def validate_phone_number(phone_number, country):
    if not phone_number:
        raise ValidationError("Phone number is required.")

    # Add phone_number_prefix if missing
    if country.phone_number_prefix and not phone_number.startswith(country.phone_number_prefix):
        phone_number = f"{country.phone_number_prefix}{phone_number}"

    # Validate phone number using regex
    if hasattr(country, 'phone_number_validator'):
        phone_number_validator = RegexValidator(
            regex=country.phone_number_validator,
            message=f"The phone number does not match the format for the selected country {country.name}. "
                    f"Expected format is: {country.phone_number_format}."
        )
        phone_number_validator(phone_number)

    # Return the potentially updated phone number with prefix
    return phone_number

def validate_business_id(business_id, country):
    if not business_id:
        # No validation needed if business_id is empty.
        return business_id

    # Validate business_id format using regex
    if country.business_id_validator:
        business_id_validator = RegexValidator(
            regex=country.business_id_validator,
            message=f"The Business ID does not match the format for the selected country {country.name}. "
                    f"Expected format is: {country.business_id_format}."
        )
        business_id_validator(business_id)

    # Return the potentially updated business_id
    return business_id

def validate_tax_id(tax_id, country):
    if not tax_id:
        # No validation needed if tax_id is empty.
        return tax_id

    # Add tax_id_prefix if missing
    if country.tax_id_prefix and not tax_id.startswith(country.tax_id_prefix):
        tax_id = f"{country.tax_id_prefix}{tax_id}"

    # Validate tax_id using regex
    if hasattr(country, 'tax_id_validator'):
        tax_id_validator = RegexValidator(
            regex=country.tax_id_validator,
            message=f"The Tax ID does not match the format for the selected country {country.name}. "
                    f"Expected format is: {country.tax_id_format}."
        )
        tax_id_validator(tax_id)

    # Return the potentially updated tax_id with prefix
    return tax_id