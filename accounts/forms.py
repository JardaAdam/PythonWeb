from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from django.forms import CharField, ModelForm, PasswordInput, ModelChoiceField
from .models import CustomUser, Company, ItemGroup


class UserRegistrationForm(ModelForm):
    password = CharField(widget=PasswordInput, label='Password')
    confirm_password = CharField(widget=PasswordInput, label='Confirm Password')
    company = ModelChoiceField(queryset=Company.objects, required=False, empty_label="-- None --",
                               label='Existing Company')

    class Meta:
        model = CustomUser
        fields = [
            'username', 'password', 'confirm_password', 'first_name', 'last_name',
            'email', 'country', 'address', 'city', 'postcode',
            'phone_number', 'business_id', 'tax_id'
        ]

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '')
        return first_name.strip().title()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '')
        return last_name.strip().title()

    """Navrh na zmenu """

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if email:
    #         validator = EmailValidator()
    #         validator(email)
    #     return email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            validator = EmailValidator()
            try:
                validator(email)
            except ValidationError as e:
                raise ValidationError(f"Zadejte platný email. Chyba: {str(e)}")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data

class UserEditForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = [  # Vyberte pole, která uživatel může upravit
            'first_name', 'last_name', 'email', 'country', 'address',
            'city', 'postcode', 'phone_number', 'business_id', 'tax_id'
        ]


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

# class ItemGroupForm(ModelForm):
#     class Meta:
#         model = ItemGroup
#         fields = ['name', 'user', 'company']
#
#     def clean(self):
#         cleaned_data = super().clean()
#         user = cleaned_data.get("user")
#         company = cleaned_data.get("company")
#
#         if not user and not company:
#             raise ValidationError('Alespoň jedno z pole user nebo company musí být vyplněné.')
#
#         return cleaned_data
