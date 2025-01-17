from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser, Company, Country


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Vytvoření testovacího uživatele a společnosti
        cls.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        cls.company = Company.objects.create(name='TestCompany')
        cls.user.company = cls.company
        cls.country = Country.objects.create(
            name='Czech Republic',
            postcode_validator=r"\d{5}",
            phone_number_prefix="+420",
            phone_number_validator=r"^(?:\+420)?\d{9}$",
            business_id_validator=r"^\d{8}$",
            tax_id_prefix="CZ",
            tax_id_validator=r"\d{10}$"
        )
        cls.user.save()

        # Přidáme dalšího uživatele pro testy, kde to bude potřeba
        cls.other_user = CustomUser.objects.create_user(username='otheruser', password='password')
        cls.other_user.company = cls.company
        cls.other_user.save()


class CustomUserViewTest(BaseTestCase):
    def test_custom_user_view_loads_correctly(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)


class CustomUserUpdateViewTest(BaseTestCase):
    def test_update_user_profile_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit_profile'), {
            'first_name': 'Updatedname',
            'last_name': 'UpdatedLastname',
            'email': self.user.email
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updatedname')

    def test_update_user_profile_failure(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit_profile'), {
            'first_name': '',  # neplatná data
            'last_name': '',
            'email': self.user.email,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')  # Zkontroluj přesné znění chybové zprávy


class CompanyListViewTest(BaseTestCase):
    def test_company_list_display(self):
        self.client.login(username='otheruser', password='password')
        response = self.client.get(reverse('company_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.company.name)


class CompanyViewTest(BaseTestCase):
    def test_access_company_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('company_detail', args=[self.company.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.company.name)


class CompanyUpdateViewTest(BaseTestCase):
    def test_successful_company_update(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit_company', args=[self.user.company.pk]), {
            'name': 'UpdatedCompanyName',
            'country': self.country.pk,
            'address': "Podebradova 712",
            'city': 'Praha',
            'postcode': '25082',
            'phone_number': '666555888',
            'business_id': '12345678',
            'tax_id': '1234567898'
        })
        if response.status_code == 200:
            print(response.context['form'].errors)  # Přidej tento řádek pro výpis chyb

        self.assertRedirects(response, reverse('company_detail', args=[self.user.company.pk]))
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, 'UpdatedCompanyName')