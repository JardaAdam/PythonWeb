# from django.forms import
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
import re

# CustomUser = get_user_model()

from .models import CustomUser, Company


# class CustomUserRegistrationForm(forms.ModelForm):
#     company_name = forms.CharField(max_length=255, required=False, help_text='Vyplňte, pokud patříte do firmy')
#
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'password', 'company_name', 'email']  # Zahrňte další požadovaná pole
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         company_name = self.cleaned_data.get('company_name')
#
#         if company_name:
#             company, _ = Company.objects.get_or_create(name=company_name)
#             user.company = company
#
#         if commit:
#             user.save()
#
#         return user
#
class SignUpForm(UserCreationForm):
    pass
#     company_name = forms.CharField(max_length=32, required=False, label="Název společnosti")
#     address = forms.CharField(max_length=128, required=False, label="Adresa")
#     city = forms.CharField(max_length=32, required=False, label="Město")
#     postcode = forms.CharField(
#         max_length=6, required=False, label="PČS",
#         widget=forms.TextInput(attrs={'placeholder': '00000'}),
#         validators=[
#             RegexValidator(
#                 regex=r'^\d{3}\s?\d{2}$',
#                 message="Poštovní směrovací číslo musí mít formát XXX XX (např. 11000 nebo 110 00)."
#             )
#         ]
#     )
#     phone_number = forms.CharField(
#         max_length=17, required=False, label="Telefonní číslo",
#         widget=forms.TextInput(attrs={'placeholder': '+420123456789'}),
#         validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Telefonní číslo musí být ve formátu: '+420123456789'. Až 15 číslic je povoleno.")]
#     )
#     ico = forms.CharField(
#         max_length=8, required=False, label="IČO",
#         widget=forms.TextInput(attrs={'placeholder': '12345678'})
#     )
#     dic = forms.CharField(
#         max_length=11, required=False, label="DIČ",
#         widget=forms.TextInput(attrs={'placeholder': 'CZ123456789'})
#     )
#
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
#
#     def clean_first_name(self):
#         first_name = self.cleaned_data.get('first_name', '')
#         return first_name.strip().title()
#
#     def clean_last_name(self):
#         last_name = self.cleaned_data.get('last_name', '')
#         return last_name.strip().title()
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if email:
#             validator = EmailValidator()
#             try:
#                 validator(email)
#             except ValidationError as e:
#                 raise ValidationError("Zadejte platný email.")
#         return email
#
#     def clean_phone_number(self):
#         phone_number = self.cleaned_data.get('phone_number', '')
#         phone_number = re.sub(r'\D', '', phone_number)  # Odstraňte všechny nečíselné znaky.
#         if len(phone_number) < 9:
#             raise ValidationError("Telefonní číslo musí obsahovat alespoň 9 číslic.")
#         return phone_number
#
#     def clean_ico(self):
#         ico = self.cleaned_data.get('ico')
#         if ico:
#             ico = re.sub(r'\D', '', ico)  # Odstraňte všechny nečíselné znaky.
#             if len(ico) != 8:
#                 raise ValidationError("IČO musí mít přesně 8 číslic.")
#         return ico
#
#     @atomic
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.company_name = self.cleaned_data['company_name']
#         user.address = self.cleaned_data['address']
#         user.city = self.cleaned_data['city']
#         user.postcode = self.cleaned_data['postcode']
#         user.phone_number = self.cleaned_data['phone_number']
#         user.ico = self.cleaned_data['ico']
#         user.dic = self.cleaned_data['dic']
#         if commit:
#             user.save()
#         return user
#
#

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