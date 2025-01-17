from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.db.transaction import atomic

from django.forms import CharField, ModelForm, PasswordInput, ModelChoiceField, Select, EmailInput, IntegerField

from .mixins import FormValidationMixin
from .models import CustomUser, Company, ItemGroup, Country
from .validators import validate_no_numbers

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



class CompanyForm(FormValidationMixin, ModelForm):
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

