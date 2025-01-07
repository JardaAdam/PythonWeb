from unittest import skip

from django.test import TestCase, Client
from django.urls import reverse

from .models import CustomUser, Country, Company


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
    @skip
    def test_redirect_to_login_if_not_logged_in(self):
        """Testuje, že nezalogovaný uživatel je přesměrován na login stránku."""
        response = self.client.get(reverse('protected_view'))  # Změňte 'protected_view' na název pohledu
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('protected_view')}")


class UserRegistrationTest(TestCase):
    # python manage.py test accounts.tests.UserRegistrationTest.test_register_user_with_company
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
            tax_id='CZ87654321'
        )

    def test_register_user_without_company(self):
        user_data = {
            'username': 'testuser',
            'password': 'SafePassword123',
            'confirm_password': 'SafePassword123',
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
            'password': 'SafePassword123',
            'confirm_password': 'SafePassword123',
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


    def test_register_user_with_company(self):
        data = {
            'username': 'testuser3',
            'password': 'SafePassword123',
            'confirm_password': 'SafePassword123',
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alicesmith@example.com',
            'country': self.country.pk,
            'address': '789 Example Street',
            'city': 'Brno',
            'postcode': '678 90',
            'phone_number': '987654321',
            'business_id': '23456789',
            'tax_id': 'CZ23456789',
        }

        company_data = {
            'name': 'Example Company',
            'country': self.country.pk,
            'address': '456 Company Ave',
            'city': 'Prague',
            'postcode': '123 45',
            'phone_number': '987654321',
            'business_id': '87654321',
            'tax_id': 'CZ87654321'
        }

        data = {**data, **company_data}

        response = self.client.post(reverse('register'), data)

        if response.status_code == 200:
            print("Validation Errors:", response.context['user_form'].errors)
        if response.status_code == 200:
            print("Validation Errors:", response.context['user_form'].errors)

        # Ověření, že registrace proběhla úspěšně a uživatel i firma byly vytvořeny
        self.assertEqual(response.status_code, 302, "Expected redirect after successful registration.")
        self.assertTrue(CustomUser.objects.filter(username='testuser3').exists(), "User was not created.")
        self.assertTrue(Company.objects.filter(name='Example Company').exists(), "Company was not created.")

    def test_register_user_with_existing_company(self):
        # Simulace dat pro nového uživatele, který se chce připojit k existující společnosti
        data = {
            'username': 'companyuser',
            'password': 'SecurePassword44',
            'confirm_password': 'SecurePassword44',
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
        self.assertEqual(user.company, self.company)  # Ověřte, že je uživatel správně přiřazen ke společnosti

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
