from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from django.forms import CharField, ModelForm, PasswordInput, ModelChoiceField, Select, EmailInput
from .models import CustomUser, Company, ItemGroup
from .validators import (
    validate_business_id,
    validate_tax_id,
    validate_phone_number,
    validate_postcode,
)

class UserRegistrationForm(ModelForm):
    # TODO doplnit empty_label pomoci prefixu z country
    password = CharField(widget=PasswordInput, label='Password')
    confirm_password = CharField(widget=PasswordInput, label='Confirm Password')
    email = CharField(widget=EmailInput, label='Email')
    company = ModelChoiceField(queryset=Company.objects,
                               required=False,
                               empty_label="Enter company name",
                               label='Existing Company',
                               widget=Select(attrs={'class': 'form-control select2'}),
                               help_text="If you haven't found your company. Create a new one after successful registration"
                               )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'password', 'confirm_password', 'first_name', 'last_name',
            'email', 'country', 'address', 'city', 'postcode',
            'phone_number', 'business_id', 'tax_id', 'company'
        ]
        widgets = {'country': Select(attrs={'class': 'form-control select2'})}

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '')
        return first_name.strip().title()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '')
        return last_name.strip().title()


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            validator = EmailValidator()
            try:
                validator(email)
            except ValidationError as e:
                raise ValidationError(f"Please enter a valid email. Error: {str(e)}")
        return email

    def clean_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()

        country = cleaned_data.get('country')
        business_id = cleaned_data.get('business_id')
        tax_id = cleaned_data.get('tax_id')
        phone_number = cleaned_data.get('phone_number')
        postcode = cleaned_data.get('postcode')

        if country:
            try:
                validate_business_id(business_id, country)
            except ValidationError as e:
                self.add_error('business_id', e.message)

            try:
                validate_tax_id(tax_id, country)
            except ValidationError as e:
                self.add_error('tax_id', e.message)

            updated_phone_number = validate_phone_number(phone_number, country)
            if updated_phone_number != phone_number:
                cleaned_data['phone_number'] = updated_phone_number

            try:
                validate_postcode(postcode, country)
            except ValidationError as e:
                self.add_error('postcode', e.message)

        return cleaned_data

class UserEditForm(ModelForm):
    company = ModelChoiceField(queryset=Company.objects,
                               required=False,
                               empty_label="Enter company name",
                               label='Existing Company',
                               widget=Select(attrs={'class': 'form-control select2'}),
                               help_text="If you haven't found your company. Create a new one after successful registration"
                               )
    class Meta:
        model = CustomUser
        fields = [  # Vyberte pole, která uživatel může upravit
            'first_name', 'last_name', 'email','company', 'country', 'address',
            'city', 'postcode', 'phone_number', 'business_id', 'tax_id'
        ]

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '')
        return first_name.strip().title()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '')
        return last_name.strip().title()


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            validator = EmailValidator()
            try:
                validator(email)
            except ValidationError as e:
                raise ValidationError(f"Please enter a valid email. Error: {str(e)}")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            'name', 'country', 'address', 'city',
            'postcode', 'phone_number', 'business_id', 'tax_id'
        ]

    def clean(self):
        cleaned_data = super().clean()
        # Další validace, pokud je potřeba
        return cleaned_data

class ItemGroupForm(ModelForm):
    class Meta:
        model = ItemGroup
        fields = ['name','user','company']


    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("user")
        company = cleaned_data.get("company")

        if not user and not company:
            raise ValidationError('Alespoň jedno z pole user nebo company musí být vyplněné.')

        return cleaned_data
