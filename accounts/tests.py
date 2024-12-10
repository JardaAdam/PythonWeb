from unittest import skip

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class AuthenticationTests(TestCase):
    def setUp(self):
        # Vytvoření uživatelského modelu a uživatele pro opakované použití v testech
        self.User = get_user_model()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'first_name': 'Jan',
            'last_name': 'Novak',
            'email': 'jan@novak.cz',
        }
        self.user = self.User.objects.create_user(**self.user_data)

    def test_login_page_loads(self):
        """Test, že stránka přihlášení se správně načte."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_with_valid_credentials(self):
        """Test, že přihlášení s platnými údaji funguje."""
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('login_success'))

    def test_login_with_invalid_credentials(self):
        """Test, že přihlášení s neplatnými údaji neprojde."""
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertContains(response, "Please enter a correct username and password.")

    def test_logout(self):
        """Test, že odhlášení funguje správně pomocí POST."""
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('index'))

        response = self.client.get(reverse('index'))
        self.assertNotContains(response, 'Hi, testuser')

    def test_signup_page_loads(self):
        """Test, že stránka registrace funguje."""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
    @skip
    def test_redirect_to_login_if_not_logged_in(self):
        """Testuje, že nezalogovaný uživatel je přesměrován na login stránku."""
        response = self.client.get(reverse('protected_view'))  # Změňte 'protected_view' na název pohledu
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('protected_view')}")


class SignUpViewTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.new_user_data = {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'first_name': 'Jan',
            'last_name': 'Novak',
            'email': 'jan@novak.cz',
            'company_name': 'Test Company',
            'address': 'Test Address',
            'city': 'Prague',
            'postcode': '12345',
            'phone_number': '+420123456789',
            'ico': '12345678',
            'dic': 'CZ123456789'
        }

    def test_signup(self):
        """Test úspěšné registrace uživatele."""
        response = self.client.post(reverse('signup'), self.new_user_data)
        self.assertRedirects(response, reverse('login_success'))
        self.assertTrue(self.User.objects.filter(username='newuser').exists())
        user = self.User.objects.get(username='newuser')
        self.assertEqual(user.company_name, 'Test Company')

