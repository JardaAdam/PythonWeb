import io
from PIL import Image
import tempfile
import shutil
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


from revisions.models import *

User = get_user_model()




class BaseViewsTest(TestCase):
    @classmethod
    # Create a new image with RGB mode and size 100x100
    def create_test_image(cls):
        file_obj = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(file_obj, 'JPEG')
        file_obj.seek(0)
        return file_obj.getvalue()

    @classmethod
    def setUpTestData(cls):
        # Nastavte dočasné úložiště pro testy
        cls.temp_media = tempfile.mkdtemp()
        settings.MEDIA_ROOT = cls.temp_media
        cls.client = Client()
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.manufacturer = Manufacturer.objects.create(name='Test Manufacturer')
        cls.material_type = MaterialType.objects.create(name='Test Material')
        cls.lifetime_of_ppe = LifetimeOfPpe.objects.create(
            manufacturer=cls.manufacturer,
            material_type=cls.material_type,
            lifetime_use_years=10,
            lifetime_manufacture_years=15
        )
        cls.type_of_ppe = TypeOfPpe.objects.create(group_type_ppe='Test Group', price=100.00)
        cls.standard_ppe = StandardPpe.objects.create(code='EN123', description='Test Standard')

        # Vytvoření a uložení obrázku
        cls.uploaded_image_content = cls.create_test_image()
        cls.uploaded_image = SimpleUploadedFile(
            "image.jpg", cls.uploaded_image_content, content_type='image/jpeg')

        # Uložení dalších dat
        cls.revision_data = RevisionData(
            image_items=cls.uploaded_image,
            lifetime_of_ppe=cls.lifetime_of_ppe,
            type_of_ppe=cls.type_of_ppe,
            name_ppe='Flash industry',
            manual_for_revision=SimpleUploadedFile("manual.pdf", b"Dummy content")
        )
        cls.revision_data.save()
        cls.revision_data.standard_ppe.add(cls.standard_ppe)
        cls.revision_data.save()

    @classmethod
    def tearDownClass(cls):
        # Odstraňte dočasné úložiště po ukončení testů
        shutil.rmtree(cls.temp_media, ignore_errors=True)
        super().tearDownClass()




    def setUp(self):
        self.client.login(username='testuser', password='testpass')

    # Pomocná metoda pro kontrolu, že je formulář neplatny
    def assert_form_invalid(self, url_name, data, expected_field_error, args=None):
        url = reverse(url_name, args=args)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn(expected_field_error, form.errors)