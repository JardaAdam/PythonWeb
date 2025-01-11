from unittest import skip

from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase, Client

from django.urls import reverse

from django.contrib.messages import get_messages
from PIL import Image
import io
from revisions.models import *

from accounts.models import CustomUser

# Create your tests here.

"""views.py"""


class BaseViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user('testuser', 'test@example.com', 'testpass')
        cls.manufacturer = Manufacturer.objects.create(name='Test Manufacturer')
        cls.material_type = MaterialType.objects.create(name='Test Material Type')
        cls.lifetime_of_ppe = LifetimeOfPpe.objects.create(
            manufacturer=cls.manufacturer,
            material_type=cls.material_type,
            lifetime_use_years=10,
            lifetime_manufacture_years=10,
        )
        cls.group_type_ppe = TypeOfPpe.objects.create(group_type_ppe='Test Group Type', price=100.00)
        cls.standard_ppe_obj = StandardPpe.objects.create(code='EN123', description='Test StandardPpe')
        cls.revision_data = RevisionData.objects.create(
            name_ppe='Example PPE',
            lifetime_of_ppe=cls.lifetime_of_ppe,
            type_of_ppe=cls.group_type_ppe,
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='testpass')


class RevisionDataTest(BaseViewTest):
    def test_create_revision_data_view(self):
        url = reverse('add_revision_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_form.html')

    def test_create_revision_data_post(self):
        url = reverse('add_revision_data')
        image_data = io.BytesIO()
        image = Image.new('RGB', (100, 100), color=(255, 0, 0))
        image.save(image_data, format='JPEG')
        image_data.seek(0)
        test_image = SimpleUploadedFile("test_image.jpg", image_data.read(), content_type="image/jpeg")
        test_file = SimpleUploadedFile("manual.txt", b"Manual content", content_type="text/plain")

        data = {
            'name_ppe': 'New PPE',
            'lifetime_of_ppe': self.lifetime_of_ppe.id,
            'type_of_ppe': self.group_type_ppe.id,
            'standard_ppe': [self.standard_ppe_obj.id],
            'image_items': test_image,
            'manual_for_revision': test_file,
        }
        response = self.client.post(url, data, follow=True)
        if response.context and response.context.get('form'):
            print(response.context['form'].errors)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertTrue(RevisionData.objects.filter(name_ppe='New PPE').exists())
        except AssertionError as e:
            print("Test failed:")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.content}")
            raise e

    def test_redirect_after_creation(self):
        url = reverse('add_revision_data') + '?next=' + reverse('revision_datas_list')
        data = {
            'name_ppe': 'Another PPE',
            'lifetime_of_ppe': self.lifetime_of_ppe.id,
            'type_of_ppe': self.group_type_ppe.id,
            'standard_ppe': [self.standard_ppe_obj.id],
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_form.html')


class RevisionRecordTest(BaseViewTest):
    def test_create_revision_record_view(self):
        url = reverse('add_revision_record')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_form.html')
        self.assertContains(response, 'Add New Revision Data')

        data = {
            'revision_data': self.revision_data.id,
            'serial_number': '1234',
            'date_manufacture': '2023-10-12',
            'date_of_first_use': '2023-10-13',
            'owner': self.user.id,
            'verdict': 'fit',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_form.html')
        self.assertContains(response, 'The item was successfully saved')
        self.assertTrue(RevisionRecord.objects.filter(serial_number='1234').exists())

    def test_create_revision_record_post(self):
        url = reverse('add_revision_record')
        data = {
            'revision_data': self.revision_data.id,
            'serial_number': '2234',
            'date_manufacture': '2023-10-12',
            'date_of_first_use': '2023-10-18',
            'owner': self.user.id,
            'verdict': 'fit',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(RevisionRecord.objects.filter(serial_number='2234').exists())

    def test_add_revision_data_button_visible(self):
        url = reverse('add_revision_record')
        response = self.client.get(url)
        self.assertContains(response, 'Add New Revision Data')


"""Přístup a Oprávnění"""


@skip
class LoginRequiredTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required_for_add_data_view(self):
        response = self.client.get(reverse('add_data'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('add_data')}")


"""Message"""


@skip
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
