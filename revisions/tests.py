from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from accounts.forms import CustomUser
from .models import StandardPpe
from .forms import StandardPpeForm

# Create your tests here.
User = get_user_model()
"""views.py"""
class AddDataViewTest(TestCase):
    def setUp(self):
        # Vytvořit uživatele a přihlásit se
        self.user = CustomUser.objects.create_user('testuser', 'test@example.com', 'testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def test_add_data_view_get(self):
        response = self.client.get(reverse('add_data'), {'model_type': 'StandardPpe'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_data.html')
        self.assertContains(response, "Add Data")

    def test_add_data_view_post_valid(self):
        response = self.client.post(reverse('add_data'), {
            'model_type': 'StandardPpe',
            'code': 'MAT123',
            'description': 'Test StandardPpe',
        })
        expected_url = f"{reverse('add_data')}?model_type=StandardPpe"  # Správně konstruovaná URL
        self.assertRedirects(response, expected_url)
        self.assertTrue(StandardPpe.objects.filter(code='MAT123').exists())

    def test_add_data_view_post_invalid(self):
        response = self.client.post(reverse('add_data'), {
            'model_type': 'StandardPpe',  # Zajištění správného model_type
            # Chybí povinné pole `code`
            'description': 'Test Material',
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIsNotNone(form)
        self.assertFalse(form.is_valid())
        self.assertIn('code', form.errors)  # kontrola, že pole `code` má chybu


"""Models"""

"""StandardPpe"""
class StandardPpeModelTest(TestCase):
    def test_string_representation(self):
        standard_ppe = StandardPpe(code='EN362', description='Test PPE')
        self.assertEqual(str(standard_ppe), 'EN362')

    def test_verbose_name(self):
        self.assertEqual(StandardPpe._meta.verbose_name, 'Standard PPE')
        self.assertEqual(StandardPpe._meta.verbose_name_plural, 'Standards PPE')

"""Forms"""

class StandardPpeFormTest(TestCase):
    def test_form_valid_data(self):
        form = StandardPpeForm(data={
            'code': 'EN362',
            'description': 'Test Description'
        })
        self.assertTrue(form.is_valid())

    def test_form_no_data(self):
        form = StandardPpeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # Očekáváme chyby pro `code` a `description`

    def test_form_invalid_code(self):
        form = StandardPpeForm(data={
            'code': '',  # Nevalidní, protože je vyžadován
            'description': 'Test Description'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('code', form.errors)


"""Přístup a Oprávnění"""


class LoginRequiredTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required_for_add_data_view(self):
        response = self.client.get(reverse('add_data'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('add_data')}")



"""Message"""

class MessageTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('testuser', 'test@example.com', 'testpass')
        self.client = Client()

    def test_success_message_displayed(self):
        logged_in = self.client.login(username='testuser', password='testpass')
        self.assertTrue(logged_in)  # Ověření úspěchu přihlášení

        # Simulace POST žádosti
        response = self.client.post(reverse('add_data'), {
            'model_type': 'StandardPpe',
            'code': 'MAT123',
            'description': 'Test StandardPpe',
        }, follow=True)  # Přidávání follow=True pro automatické sledování přesměrování

        # Získání zpráv po přesměrování
        messages = list(get_messages(response.wsgi_request))

        # Debugging: Výpis všech zpráv pro kontrolu
        print(f"Found {len(messages)} message(s).")
        for message in messages:
            print(f"Message: {str(message)}")

        # Ověření, že je jedna zpráva a je správná
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'The item was successfully saved.')