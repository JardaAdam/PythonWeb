from unittest import skip
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class AuthenticationTests(TestCase):

    def test_login_page_loads(self):
        """Test, že stránka přihlášení se správně načte"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_with_valid_credentials(self):
        """Test, že přihlášení s platnými údaji funguje"""
        user = User.objects.create_user(username='testuser', password='testpassword')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('index'))
    @skip
    def test_login_with_invalid_credentials(self):
        """Test, že přihlášení s neplatnými údaji neprojde"""
        user = User.objects.create_user(username='testuser', password='testpassword')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertFormError(response, 'form', 'password', 'This password is incorrect.')
    @skip
    def test_logout(self):
        """Test, že odhlášení funguje"""
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('index'))
        # Ověření, že uživatel je odhlášen
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, 'Hi, testuser')

    def test_signup_page_loads(self):
        """Test, že stránka registrace funguje"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
    @skip
    def test_successful_signup(self):
        """Test úspěšné registrace uživatele"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
            'first_name': 'Jan',
            'last_name': 'Novak',
            'email': 'jan@novak.cz',
        })
        self.assertRedirects(response, reverse('index'))
        user = get_user_model().objects.get(username='newuser')
        self.assertTrue(user.is_active)
    @skip
    def test_signup_with_mismatched_passwords(self):
        """Test, že registrace selže, když hesla neodpovídají"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'wrongpassword',
            'first_name': 'Jan',
            'last_name': 'Novak',
            'email': 'jan@novak.cz',
        })
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')
