""" tento soubor si vytvorim rucne """
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.db.transaction import atomic
from django.forms import DateField, NumberInput, CharField, PasswordInput, Textarea, DecimalField
from accounts.models import Profile


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
    state = CharField(
        max_length=32,
        required=False,
        label="Stát"
    )
    phone_number = CharField(
        max_length=17,
        required=False,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Telefonní číslo musí být ve formátu: '+420123456789'. Až 15 číslic je povoleno.")],
        label="Telefonní číslo"
    )
    ICO = CharField(
        max_length=32,
        required=False,
        label="IČO"
    )
    DIC = CharField(
        max_length=32,
        required=False,
        label="DIČ"
    )


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