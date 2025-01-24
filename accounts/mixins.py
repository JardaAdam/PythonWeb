import logging

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ValidationError

from .validators import (
    validate_address,
    validate_postcode,
    validate_phone_number,
    validate_business_id,
    validate_tax_id,


)


class FormValidationMixin:
    """This method validates address, postcode, phone number, business ID, and tax ID."""

    def clean(self):
        cleaned_data = super().clean()

        country = cleaned_data.get('country')
        address = cleaned_data.get('address')
        postcode = cleaned_data.get('postcode')
        phone_number = cleaned_data.get('phone_number')
        business_id = cleaned_data.get('business_id')
        tax_id = cleaned_data.get('tax_id')

        # Validace address
        try:
            validated_address = validate_address(address)
            cleaned_data['address'] = validated_address
        except ValidationError as e:
            self.add_error('address', e.message)

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
                cleaned_data['tax_id'] = updated_tax_id
            except ValidationError as e:
                self.add_error('tax_id', e.message)

        return cleaned_data


class LoggerMixin:
    """
    Mixin pro poskytnutí základní funkcionality pro logování v rámci tříd.
    """
    @property
    def logger(self):
        # Vytvoří logger specifický pro tuto třídu
        logger_name = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return logging.getLogger(logger_name)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)


class PermissionStaffMixin(UserPassesTestMixin, LoggerMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='RevisionTechnician').exists()

    def handle_no_permission(self):
        self.log_warning(f"Unauthorized access attempt by user ID {self.request.user.id}")
        return super().handle_no_permission()

