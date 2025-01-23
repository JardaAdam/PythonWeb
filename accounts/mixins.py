import logging

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ValidationError

from .validators import (
    validate_business_id,
    validate_tax_id,
    validate_phone_number,
    validate_postcode,
)

class FormValidationMixin:
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

    def add_context_data(self, context):
        context['can_view_restricted'] = self.test_func()
        print(f"Added to context: can_view_restricted = {context['can_view_restricted']}")  # Debugovací výstup