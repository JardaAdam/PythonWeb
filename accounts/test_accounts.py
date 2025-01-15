from unittest import skip

from django.test import TestCase, Client
from django.urls import reverse

from .forms import UserRegistrationForm
from .models import CustomUser, Country, Company


class UserRegistrationFormTest(TestCase):

    def setUp(self):
        # Vytvoření testovací instance Country
        self.country = Country.objects.create(name="Testland",
                                              postcode_validator=r"\d{5}",
                                              phone_number_prefix="+420",
                                              phone_number_validator=r"^(?:\+420)?\d{9}$",
                                              business_id_validator=r"^\d{8}$",
                                              tax_id_prefix="CZ",
                                              tax_id_validator=r"\d{10}$"
                                              )

    def test_valid_data(self):
        form = UserRegistrationForm(data={
            'username': 'testuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'country': self.country.id,
            'address': '123 Test Street',
            'city': 'Test City',
            'postcode': '12345',
            'phone_number': '123456789',
            'business_id': '12345678',
            'tax_id': '0123456789',
            'company': None,
        })

        self.assertTrue(form.is_valid())

    def test_mismatched_passwords(self):
        form = UserRegistrationForm(data={
            'username': 'testuser',
            'password1': 'strongpassword123',
            'password2': 'anotherpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'country': self.country.id,
            'address': '123 Test Street',
            'city': 'Test City',
            'postcode': '12345',
            'phone_number': '123456789',
            'business_id': 'TL-123456',
            'tax_id': 'TL-123456',
            'company': None,
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ["Passwords do not match."])

    def test_invalid_phone_number(self):
        form = UserRegistrationForm(data={
            'username': 'testuser',
            'password': 'strongpassword123',
            'confirm_password': 'strongpassword123',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'country': self.country.id,
            'address': '123 Test Street',
            'city': 'Test City',
            'postcode': '12345',
            'phone_number': '12345',  # Invalid phone number
            'business_id': '12345678',
            'tax_id': 'CZ1234567890',
            'company': None,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)

    def test_missing_tax_id_prefix(self):
        form = UserRegistrationForm(data={
            'username': 'testuser',
            'password': 'strongpassword123',
            'confirm_password': 'strongpassword123',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'country': self.country.id,
            'address': '123 Test Street',
            'city': 'Test City',
            'postcode': '12345',
            'phone_number': '123456789',
            'business_id': 'TL-123456',
            'tax_id': '123456',  # Missing prefix
            'company': None,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('tax_id', form.errors)


class UserLoginTest(TestCase):
    def setUp(self):
        # Vytvoření uživatele pro autentizaci během testu
        self.username = 'testuser'
        self.password = 'SafePassword123'  # nastavit heslo
        self.user = CustomUser.objects.create_user(
            username=self.username,
            password=self.password,
            email='testuser@example.com'
        )

    def test_user_creation(self):
        # Ověřte, že uživatel byl vytvořen
        self.assertIsNotNone(self.user)
        self.assertTrue(self.user.check_password('SafePassword123'))

    def test_login_page_loads(self):
        """Test, že stránka přihlášení se správně načte."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_with_valid_credentials(self):
        # Přihlášení s platnými údaji
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })

        # Ověření, zda došlo k redirect na "login_success"
        self.assertRedirects(response, reverse('login_success'))

    def test_login_with_invalid_credentials(self):
        """Test, že přihlášení s neplatnými údaji neprojde."""
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertContains(response, "Please enter a correct username and password.")

    def test_logout(self):
        """Test, že odhlášení funguje správně pomocí POST."""
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('home'))

        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'Hi, testuser')

    def test_register_page_loads(self):
        """Test, že stránka registrace funguje."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_login_if_not_logged_in(self):
        """Testuje, že nezalogovaný uživatel je přesměrován na login stránku."""
        # Předpokládejme, že 'protected_view' je view chráněný pomocí LoginRequiredMixin
        response = self.client.get(reverse('profile'))

        # Kontrola přesměrování na login stránku
        expected_redirect_url = f"{reverse('login')}?next={reverse('profile')}"
        self.assertRedirects(response, expected_redirect_url)


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        # Vytvoření potřebných objekty, jako je Country
        self.country = Country.objects.create(
            name='Czech Republic',
            language_code='cs',
            postcode_format=r'^\d{3}\s?\d{2}$',
            phone_number_prefix='+420',
            business_id_format=r'\d{8}',
            tax_id_format=r'CZ\d{8,10}',
        )

        self.company = Company.objects.create(
            name='ExampleCorp',
            country=self.country,
            address='789 Example Road',
            city='Ostrava',
            postcode='700 30',
            phone_number='987654321',
            business_id='87654321',
            tax_id='CZ9876543210'
        )

    def test_register_user_without_company(self):
        user_data = {
            'username': 'testuser',
            'password1': 'SafePassword123',
            'password2': 'SafePassword123',
            'first_name': 'jane',
            'last_name': 'doe',
            'email': 'janedoe@example.com',
            'country': self.country.pk,
            'address': '456 Example Street',
            'city': 'Prague',
            'postcode': '123 45',
            'phone_number': '123456789',
            'business_id': '12345678',
            'tax_id': 'CZ12345678',}

        response = self.client.post(reverse('register'), user_data)


        # Ověření, že registrace proběhla úspěšně a uživatel byl vytvořen
        self.assertEqual(response.status_code, 302)  # Presmerovani po uspesne registraci
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists(), "User was not created.")

        # Ověření dat uživatele
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.first_name, 'Jane')  # Předpokládáme, že clean je formátuje
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.com')
        self.assertEqual(user.country, self.country)  # Porovnáváme FK objekty
        self.assertEqual(user.address, '456 Example Street')
        self.assertEqual(user.city, 'Prague')
        self.assertEqual(user.postcode, '123 45')
        self.assertEqual(user.phone_number, '+420123456789')
        self.assertEqual(user.business_id, '12345678')
        self.assertEqual(user.tax_id, 'CZ12345678')

    def test_register_user_with_invalid_postcode(self):
        # Ukázkový test pro nesprávný formát PSČ
        user_data = {
            'username': 'testuser2',
            'password1': 'SafePassword123',
            'password2': 'SafePassword123',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.com',
            'country': self.country.pk,
            'address': '456 Example Street',
            'city': 'Brno',
            'postcode': 'invalid',  # Nesprávné PSČ
            'phone_number': '123456789',
            'business_id': '87654321',
            'tax_id': 'CZ87654321'}

        response = self.client.post(reverse('register'), user_data)

        # Ověření, že registrace selhala
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(username='testuser2').exists(),
                         "User should not be created with invalid postcode.")


    def test_register_user_with_existing_company(self):
        # Simulace dat pro nového uživatele, který se chce připojit k existující společnosti
        data = {
            'username': 'companyuser',
            'password1': 'SecurePassword44',
            'password2': 'SecurePassword44',
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alicesmith@example.com',
            'country': self.country.pk,
            'address': '101 Example Avenue',
            'city': 'Brno',
            'postcode': '608 00',
            'phone_number': '777123456',
            'business_id': '23456789',
            'tax_id': 'CZ23456789',
            'company': self.company.pk  # ID existující společnosti
        }

        response = self.client.post(reverse('register'), data)

        # Výpis chyb formuláře, pokud existují
        if response.status_code == 200:
            print(response.context['user_form'].errors)
            print(response.context['company_form'].errors)

        # Ověření, že uživatel je úspěšně přesměrován (HTTP status 302) po úspěšné registraci
        self.assertEqual(response.status_code, 302)

        # Ověření, že uživatel je vytvořen v databázi a patří do správné společnosti
        user = CustomUser.objects.get(username='companyuser')
        self.assertIsNotNone(user)
        self.assertEqual(user.company, self.company)

    def test_register_user_with_conflicting_data(self):
        # Tento test simuluje scénář, kdy dojde k konfliktu při tvorbě uživatele
        data = {
            'username': 'dupuser',
            'password': 'SecurePassword44',
            'confirm_password': 'SecurePassword44',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'conflict@domain.com',
            'country': self.country.pk,
            'address': '456 Conflict Ave',
            'city': 'Prague',
            'postcode': '123 45',
            'phone_number': '987654321',
            'business_id': '12345678',
            'tax_id': 'CZ12345678',
            'company': self.company.pk
        }

        # Vytvoření uživatele se stejným uživatelským jménem pro vyvolání IntegrityError
        CustomUser.objects.create(
            username='dupuser',
            email='conflict@domain.com',
            company=self.company
        )

        response = self.client.post(reverse('register'), data)

        # Ověření, že registrace selže, formulář má chyby
        self.assertEqual(response.status_code, 200)
        self.assertIn("A user with that username already exists.", str(response.content))
