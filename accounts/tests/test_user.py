from datetime import date
from unittest import skip

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse

from accounts.forms import UserRegistrationForm
from accounts.models import CustomUser, Country, Company
from config.test_base_view import BaseViewsTest
from revisions.models import RevisionRecord

User = get_user_model()


class BaseTestSetup(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Nastavení společné pro všechny testovací třídy
        # Vytváří skupinu `Company Supervisor` pro testování
        cls.company_supervisor_group, created = Group.objects.get_or_create(name='CompanySupervisor')
        cls.country = Country.objects.create(
            name='Czech Republic',
            postcode_validator=r"\d{5}",
            phone_number_prefix="+420",
            phone_number_validator=r"^(?:\+420)?\d{9}$",
            business_id_validator=r"^\d{8}$",
            tax_id_prefix="CZ",
            tax_id_validator=r"\d{10}$"
        )

        cls.company = Company.objects.create(
            name='ExampleCorp',
            country=cls.country,
            address='789 Example Road',
            city='Ostrava',
            postcode='70030',
            phone_number='987654321',
            business_id='87654321',
            tax_id='CZ9876543210'
        )

        cls.username = 'testuser'
        cls.password = 'SafePassword123'
        cls.user = CustomUser.objects.create_user(
            username=cls.username,
            password=cls.password,
            email='testuser@example.com'
        )


class UserRegistrationFormTest(BaseTestSetup):
    def test_valid_data(self):
        form = UserRegistrationForm(data={
            'username': 'testuser2',
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


class UserRegistrationTest(BaseTestSetup):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    def test_register_user_without_company(self):
        user_data = {
            'username': 'testuser1',
            'password1': 'SafePassword123',
            'password2': 'SafePassword123',
            'first_name': 'jane',
            'last_name': 'doe',
            'email': 'janedoe@example.com',
            'country': self.country.pk,
            'address': 'Example Street 456',
            'city': 'Prague',
            'postcode': '12345',
            'phone_number': '123456789',
            'business_id': '12345678',
            'tax_id': 'CZ1234567890', }

        response = self.client.post(reverse('register'), user_data)

        # Ověření, že registrace proběhla úspěšně a uživatel byl vytvořen
        self.assertEqual(response.status_code, 302)  # Presmerovani po uspesne registraci
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists(), "User was not created.")

        # Ověření dat uživatele
        user = CustomUser.objects.get(username='testuser1')
        self.assertEqual(user.first_name, 'Jane')  # Předpokládáme, že clean je formátuje
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.com')
        self.assertEqual(user.country, self.country)  # Porovnáváme FK objekty
        self.assertEqual(user.address, 'Example street 456')
        self.assertEqual(user.city, 'Prague')
        self.assertEqual(user.postcode, '12345')
        self.assertEqual(user.phone_number, '+420123456789')
        self.assertEqual(user.business_id, '12345678')
        self.assertEqual(user.tax_id, 'CZ1234567890')

    def test_signal_assigns_company_supervisor_group(self):
        # Zajistí, že nový uživatel bez přiřazené společnosti získá skupinu `Company Supervisor`
        user = CustomUser.objects.create_user(
            username='testuser_no_company',
            password='SafePassword123',
            email='testuser_no_company@example.com',
            first_name='Signal',
            last_name='Signalovic',
            country=self.country,
            address='123 Test Street',
            city='Test City',
            postcode='12345',
            phone_number='+420123456789',
            business_id='12345678',
            tax_id='CZ1234567890',
            company=None  # Žádná společnost, takže signál by měl skupinu přiřadit
        )

        # Ověření, že uživatelská skupina je správně aplikována
        self.assertIn(self.company_supervisor_group, user.groups.all())

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
            'postcode': '60800',
            'phone_number': '777123456',
            'business_id': '23456789',
            'tax_id': 'CZ2345678901',
            'company': self.company.pk  # ID existující společnosti
        }

        response = self.client.post(reverse('register'), data)

        # Výpis chyb formuláře, pokud existují
        if response.status_code == 200:
            print(response.context['user_form'].errors)
            # print(response.context['company_form'].errors)

        # Ověření, že uživatel je úspěšně přesměrován (HTTP status 302) po úspěšné registraci
        self.assertEqual(response.status_code, 302)

        # Ověření, že uživatel je vytvořen v databázi a patří do správné společnosti
        user = CustomUser.objects.get(username='companyuser')
        self.assertIsNotNone(user)
        self.assertEqual(user.company, self.company)

    def test_register_user_with_existing_company_assigned_company_user_group(self):
        # Data pro uživatele, který se připojí k existující společnosti
        data = {
            'username': 'existingcompanyuser',
            'password1': 'SecurePassword44',
            'password2': 'SecurePassword44',
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'email': 'bob@example.com',
            'country': self.country.pk,
            'address': '123 Existing Way',
            'city': 'Existing City',
            'postcode': '60606',
            'phone_number': '987654321',
            'business_id': '87654321',
            'tax_id': 'CZ8765432145',
            'company': self.company.pk  # ID existující společnosti
        }

        response = self.client.post(reverse('register'), data)

        # Zkontroluj, že registrace je úspěšná (302 Redirection)
        self.assertEqual(response.status_code, 302)

        # Ověření, že uživatel byl vytvořen
        user = CustomUser.objects.get(username='existingcompanyuser')
        self.assertEqual(user.company, self.company)

        # Připravení a ověření, že uživatel je ve skupině CompanyUser
        company_user_group, _ = Group.objects.get_or_create(name='CompanyUser')
        self.assertIn(company_user_group, user.groups.all())

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


class PasswordResetTest(BaseViewsTest):
    def setUp(self):
        self.revision_record = RevisionRecord.objects.create(
            revision_data=self.revision_data,
            serial_number='SN12345',
            date_manufacture=date.today(),
            date_of_first_use=date.today(),
            owner=self.user,
            verdict='fit',
            created_by=self.user)

        self.revision_record.save()

    def test_password_reset_with_correct_security_questions(self):
        response = self.client.post(reverse('forgot_password'), {
            'username': 'testuser',
            'helmet_name': ['Flash industry'],
            'helmet_manufacturer': ['Test Manufacturer'],
        })

        # Očekáváme přesměrování na reset hesla
        self.assertRedirects(response, reverse('password_reset', args=[self.user.id]))

    def test_password_reset_with_incorrect_helmet_name(self):
        response = self.client.post(reverse('forgot_password'), {
            'username': 'testuser',
            'helmet_name': 'Incorrect Helmet',
            'helmet_manufacturer': 'Test Manufacturer',
        })

        # Očekáváme, že formulář obsahuje chybu na poli helmet_name
        form = response.context['form']
        self.assertIn('helmet_name', form.errors)
        self.assertIn("Incorrect helmet name.", form.errors['helmet_name'])

    def test_password_reset_with_incorrect_username(self):
        response = self.client.post(reverse('forgot_password'), {
            'username': 'wronguser',
            'helmet_name': 'Test Helmet',
            'helmet_manufacturer': 'Test Manufacturer',
        })

        # Očekáváme, že formulář obsahuje chybu na poli username
        form = response.context['form']
        self.assertIn('username', form.errors)
        self.assertIn("User with this username does not exist.", form.errors['username'])


class CompanyUserPermissionTest(TestCase):
    def setUp(self):
        # Příprava prostředí testu
        self.client = Client()

        # Vytvoření skupiny CompanyUser pro testování
        self.company_user_group, _ = Group.objects.get_or_create(name='CompanyUser')

        self.country = Country.objects.create(name='Testland')
        self.company = Company.objects.create(name='TestCorp', country=self.country)

        # Vytvoření uživatele s rolí CompanyUser
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com',
            company=self.company
        )
        self.user.groups.add(self.company_user_group)

    def test_company_user_cannot_edit_company(self):
        self.client.login(username='testuser', password='password123')

        response = self.client.get(reverse('edit_company', args=[self.company.pk]))

        # Ověření, že uživatel obdrží 403 Forbidden při pokusu o úpravu
        self.assertEqual(response.status_code, 403)

    def test_company_user_can_see_their_companies_item_groups(self):
        # Přihlášení uživatele
        self.client.login(username='testuser', password='password123')

        # Simulace zobrazení ItemGroups, které patří k jeho společnosti
        response = self.client.get(reverse('item_group_company_list'))

        # Ověření, že uživatel může vidět ItemGroups své společnosti
        self.assertEqual(response.status_code, 200)
        # Zkontroluj, že v šabloně jsou správné data (můžeš přizpůsobit podle potřeby)
        # self.assertContains(response, "Item Group 1")