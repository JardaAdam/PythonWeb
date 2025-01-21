from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.db.models import ImageField
from django.db.transaction import atomic

from django.forms import CharField, ModelForm, PasswordInput, ModelChoiceField, Select, EmailInput, Form
from django.template.defaultfilters import default

from revisions.models import RevisionRecord
from .mixins import FormValidationMixin
from .models import CustomUser, Company, ItemGroup, Country
from .validators import validate_no_numbers


""" PASSWORD RESET """
class SecurityQuestionForm(Form):
    username = CharField(label="Username", max_length=150)
    helmet_name = CharField(label="What is the name of your helmet?", max_length=255)
    helmet_manufacturer = CharField(label="Who is the manufacturer of your helmet?", max_length=255)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        helmet_name = cleaned_data.get("helmet_name")
        helmet_manufacturer = cleaned_data.get("helmet_manufacturer")

        user = get_user_model()

        try:
            user = user.objects.get(username__iexact=username)
        except user.DoesNotExist:
            self.add_error('username', "User with this username does not exist.")
            return cleaned_data

        revision_records = RevisionRecord.objects.filter(owner=user)
        helmet_name_match = revision_records.filter(revision_data__name_ppe__iexact=helmet_name).exists()
        helmet_manufacturer_match = revision_records.filter(
            revision_data__lifetime_of_ppe__manufacturer__name__iexact=helmet_manufacturer
        ).exists()

        if not helmet_name_match:
            self.add_error('helmet_name', "Incorrect helmet name.")
        if not helmet_manufacturer_match:
            self.add_error('helmet_manufacturer', "Incorrect helmet manufacturer name.")

        return cleaned_data

class PasswordResetForm(Form):
    new_password = CharField(widget=PasswordInput, label='New Password')
    confirm_password = CharField(widget=PasswordInput, label='Confirm New Password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match!")


""" USER """
class UserRegistrationForm(FormValidationMixin, ModelForm):
    password1 = CharField(widget=PasswordInput, label='Password')
    password2 = CharField(widget=PasswordInput, label='Confirm Password')
    first_name = CharField(max_length=40, required=True, validators=[validate_no_numbers])
    last_name = CharField(max_length=40, required=True, validators=[validate_no_numbers])
    email = CharField(widget=EmailInput, label='Email')
    country = ModelChoiceField(required=True, queryset=Country.objects)
    address = CharField(max_length=128, required=True)
    city = CharField(max_length=32, required=True)
    postcode = CharField(max_length=6, required=True)
    phone_number = CharField(max_length=20, required=True)
    # FIXME upravyt zobrazeni firmy doplnit o City aby se upresnilo odkud firma je kdyby bylo vice firem se stejnym nazvem
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
            'username', 'password1', 'password2', 'first_name', 'last_name',
            'email', 'country', 'address', 'city', 'postcode',
            'phone_number', 'business_id', 'tax_id', 'company'
        ]
        widgets = {'country': Select(attrs={'class': 'form-control select2'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            ''' Default set country Czech Republic'''
            default_country = Country.objects.get(name='Czech Republic')
            self.fields['country'].initial = default_country.id
        except Country.DoesNotExist:
            pass  # Pro případ, že CZ země neexistuje, tento krok by měl být promyšleně řešen v produkci

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
    # TODO def clean_address(self): adresaa musi obsahovat i cisla domu


    # TODO def clean_city(self): zvetsit prvni pismeno, pouze pismena


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error('password2', "Passwords do not match.")

        return cleaned_data

    @atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user


class CustomUserUpdateForm(FormValidationMixin, ModelForm):
    first_name = CharField(max_length=40, required=True, validators=[validate_no_numbers])
    last_name = CharField(max_length=40, required=True, validators=[validate_no_numbers])
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
            'first_name', 'last_name', 'email', 'company', 'country', 'address',
            'city', 'postcode', 'phone_number', 'business_id', 'tax_id'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            ''' Default set country Czech Republic'''
            default_country = Country.objects.get(name='Czech Republic')
            self.fields['country'].initial = default_country.id
        except Country.DoesNotExist:
            pass  # Pro případ, že CZ země neexistuje, tento krok by měl být promyšleně řešen v produkci

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

""" COMPANY """
class CompanyForm(FormValidationMixin, ModelForm):
    logo = ImageField()
    name = CharField(required=True, validators=[validate_no_numbers])
    country = ModelChoiceField(required=True, queryset=Country.objects)
    address = CharField(max_length=128, required=True)
    city = CharField(max_length=32, required=True)
    postcode = CharField(max_length=6, required=True)
    phone_number = CharField(max_length=20, required=True)
    business_id = CharField(required=True)
    tax_id = CharField(required=True)

    class Meta:
        model = Company
        fields = [
            'logo', 'name', 'country', 'address', 'city',
            'postcode', 'phone_number', 'business_id', 'tax_id'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            ''' Default set country Czech Republic'''
            default_country = Country.objects.get(name='Czech Republic')
            self.fields['country'].initial = default_country.id
        except Country.DoesNotExist:
            print("Default country does not exist in the database.")
    # TODO def clean_name(self): zvetsit prvni pismeno

    # TODO def clean_address(self): adresaa musi obsahovat i cisla domu

    # TODO def clean_city(self): zvetsit prvni pismeno, pouze pismena



    def clean(self):
        cleaned_data = super().clean()
        # Další validace, pokud je potřeba
        return cleaned_data

""" ITEM GROUP """
class ItemGroupForm(ModelForm):
    class Meta:
        model = ItemGroup
        fields = '__all__'
        widgets = {'user': Select(attrs={'class': 'form-control select2'}),
                   'company': Select(attrs={'class': 'form-control select2'})
                   }

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("user")
        company = cleaned_data.get("company")

        if not user and not company:
            raise ValidationError('Alespoň jedno z pole user nebo company musí být vyplněné.')

        return cleaned_data
