from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm
from django.views.generic.edit import ModelFormMixin

from .validators import (
    validate_business_id,
    validate_tax_id,
    validate_phone_number,
    validate_postcode,
)

class FormValidationMixin(ModelForm):
    """ This method validate address and Tax_id, Business ID"""
    def clean(self):
        cleaned_data = super().clean()

        country = cleaned_data.get('country')
        postcode = cleaned_data.get('postcode')
        phone_number = cleaned_data.get('phone_number')
        business_id = cleaned_data.get('business_id')
        tax_id = cleaned_data.get('tax_id')

        if country:
            # Validace postcode
            try:
                validate_postcode(postcode, country)
            except ValidationError as e:
                self.add_error('postcode', e.message)
                # Validace phone number
            try:
                updated_phone_number = validate_phone_number(phone_number, country)
                if updated_phone_number != phone_number:
                    cleaned_data['phone_number'] = updated_phone_number
            except ValidationError as e:
                self.add_error('phone_number', e.message)
            # Validace business ID
            try:
                validate_business_id(business_id, country)
            except ValidationError as e:
                self.add_error('business_id', e.message)

            # Validace tax ID
            try:
                updated_tax_id = validate_tax_id(tax_id, country)
                cleaned_data['tax_id'] = updated_tax_id  # Uložení aktualizovaného tax_id do cleaned_data
            except ValidationError as e:
                self.add_error('tax_id', e.message)

        return cleaned_data