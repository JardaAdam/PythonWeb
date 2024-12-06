""" tento soubor si vytvorim rucne """
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.db.transaction import atomic
from django.forms import DateField, NumberInput, CharField, PasswordInput, Textarea, DecimalField, TextInput
from accounts.models import Profile

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator




import re

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Uživatelské jméno',
            'first_name': 'Jméno',
            'last_name': 'Příjmení',
            'email': 'email'
        }

    password1 = CharField(
        widget=PasswordInput(attrs={'placeholder': 'Heslo'}),
        label="Heslo"
    )
    password2 = CharField(
        widget=PasswordInput(attrs={'placeholder': 'Heslo znovu'}),
        label="Heslo znovu"
    )
    # Pole pro profil
    company_name = CharField(
        max_length=32,
        required=False,
        label="Název společnosti"
    )
    address = CharField(
        max_length=128,
        required=False,
        label="Adresa"
    )
    city = CharField(
        max_length=32,
        required=False,
        label="Město"
    )
    postcode = CharField(
        max_length=6,
        widget=TextInput(attrs={
            'placeholder': '00000'}),  # Šedá nápověda
        required=False,
        label="PČS"
    )
    phone_number = CharField(
        max_length=17,
        required=False,
        widget=TextInput(attrs={
            'placeholder': '+420123456789'}),
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Telefonní číslo musí být ve formátu: '+420123456789'. Až 15 číslic je povoleno.")],
        label="Telefonní číslo"
    )
    ICO = CharField(
        max_length=8,
        widget=TextInput(attrs={
            'placeholder': '12345678'}),
        required=False,
        label="IČO"
    )
    DIC = CharField(
        max_length=11,
        widget=TextInput(attrs={
            'placeholder': 'CZ123456789'}),
        required=False,
        label="DIČ"
    )

    # Validace pro jméno - první písmeno velké
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            first_name = first_name.strip().title()  # .title() zvětší první písmeno
        return first_name

    # Validace pro příjmení - první písmeno velké
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            last_name = last_name.strip().title()  # .title() zvětší první písmeno
        return last_name

    # Přidání validace pro email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Můžete přidat vlastní logiku pro validaci emailu
        if email:
            validator = EmailValidator()
            try:
                validator(email)
            except ValidationError:
                raise ValidationError("Zadejte platný email.")
        return email

    # Validace pro telefonní číslo (formátování)
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Pokud telefonní číslo není prázdné, ošetříme formát
            phone_number = re.sub(r'\D', '', phone_number)  # Odstraní všechny nečíselné znaky
            if len(phone_number) < 9:
                raise ValidationError("Telefonní číslo musí obsahovat alespoň 9 číslic.")
            return phone_number
        return phone_number

    def clean_ICO(self):
        ico = self.cleaned_data.get('ICO')
        if ico:
            # Odstranění všech nečíselných znaků (pokud by uživatel zadal mezery nebo jiné znaky)
            ico = re.sub(r'\D', '', ico)
            # Validace délky IČO (mělo by mít přesně 8 číslic)
            if len(ico) != 8:
                raise ValidationError("IČO musí mít přesně 8 číslic.")
            return ico
        return ico

    @atomic # tato metoda hlida konflikty kdyby dva lidi delali registraci naraz
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit=False) # Neukládáme uživatele ihned
        company_name = self.cleaned_data['company_name']
        address = self.cleaned_data['address']
        city = self.cleaned_data['city']
        state = self.cleaned_data['state']
        phone_number = self.cleaned_data['phone_number']
        ICO = self.cleaned_data['ICO']
        DIC = self.cleaned_data['DIC']

        profile = Profile(user=user,
                          company_name=company_name,
                          address=address,
                          city=city,
                          state=state,
                          phone_number=phone_number,
                          ICO=ICO,
                          DIC=DIC)

        if commit:
            user.save() # Uložíme uživatele
            profile.save() # Uložíme profil
        return user

