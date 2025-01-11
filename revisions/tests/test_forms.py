from datetime import *

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image
import io
from accounts.models import ItemGroup
from django.contrib.auth import get_user_model
from revisions.forms import RevisionDataForm, ManufacturerForm, StandardPpeForm, MaterialTypeForm, TypeOfPpeForm, \
    RevisionRecordForm
from revisions.models import TypeOfPpe, LifetimeOfPpe, MaterialType, Manufacturer, RevisionData

User = get_user_model()

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


class BaseFormTest(TestCase):
    @classmethod
    def create_test_image(cls):
        img = Image.new('RGB', (100, 100), color='red')
        byte_arr = io.BytesIO()
        img.save(byte_arr, format='JPEG')  # Uloží jako JPEG
        return byte_arr.getvalue()

    @classmethod
    def setUpTestData(cls):
        # Common setup that can be used across form tests
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        cls.material_type = MaterialType.objects.create(name="Test Material")
        cls.lifetime_of_ppe = LifetimeOfPpe.objects.create(
            manufacturer=cls.manufacturer,
            material_type=cls.material_type,
            lifetime_use_years=10,
            lifetime_manufacture_years=15
        )
        cls.type_of_ppe = TypeOfPpe.objects.create(group_type_ppe='Test Group', price=100.00)
class FormWithImageTest(BaseFormTest):

    def test_material_type_form_with_image(self):
        image_content = self.create_test_image()
        uploaded_image = SimpleUploadedFile("material_image.jpg", image_content, content_type="image/jpeg")
        form_data = {'name': 'Test Material Type'}
        form = MaterialTypeForm(data=form_data, files={'symbol': uploaded_image})

        self.assertTrue(form.is_valid())

    def test_standard_ppe_form_with_image(self):
        image_content = self.create_test_image()
        uploaded_image = SimpleUploadedFile("ppe_image.jpg", image_content, content_type="image/jpeg")
        form_data = {'code': 'EN123', 'description': 'Test PPE Standard'}
        form = StandardPpeForm(data=form_data, files={'image': uploaded_image})

        self.assertTrue(form.is_valid())

    def test_manufacturer_form_with_logo(self):
        image_content = self.create_test_image()
        uploaded_image = SimpleUploadedFile("manufacturer_logo.jpg", image_content, content_type="image/jpeg")
        form_data = {'name': 'Test Manufacturer'}
        form = ManufacturerForm(data=form_data, files={'logo': uploaded_image})

        self.assertTrue(form.is_valid())

    def test_type_of_ppe_form_with_image(self):
        image_content = self.create_test_image()
        uploaded_image = SimpleUploadedFile("type_of_ppe_image.jpg", image_content, content_type="image/jpeg")
        form_data = {'group_type_ppe': 'Test Group', 'price': 100.00}
        form = TypeOfPpeForm(data=form_data, files={'image': uploaded_image})

        self.assertTrue(form.is_valid())

    def test_revision_data_form_with_files(self):
        image_content = self.create_test_image()
        uploaded_image = SimpleUploadedFile("revision_image.jpg", image_content, content_type="image/jpeg")
        uploaded_document = SimpleUploadedFile("manual.pdf", b"dummy content", content_type="application/pdf")
        form_data = {
            'name_ppe': 'Valid PPE',
            'lifetime_of_ppe': self.lifetime_of_ppe.id,
            'type_of_ppe': self.type_of_ppe.id
        }
        form = RevisionDataForm(data=form_data, files={
            'image_items': uploaded_image,
            'manual_for_revision': uploaded_document
        })

        self.assertTrue(form.is_valid())

    def test_revision_record_form_with_image(self):
        image_content = self.create_test_image()
        uploaded_image = SimpleUploadedFile("record_image.jpg", image_content, content_type="image/jpeg")
        revision_data = RevisionData.objects.create(
            image_items=uploaded_image,
            lifetime_of_ppe=self.lifetime_of_ppe,
            type_of_ppe=self.type_of_ppe,
            name_ppe='Test PPE',
            manual_for_revision=SimpleUploadedFile("manual1.pdf", b"dummy content", content_type="application/pdf"),
        )
        form_data = {
            'revision_data': revision_data.id,
            'serial_number': 'SN12345',
            'date_manufacture': timezone.now().date(),
            'owner': self.user.id
        }
        form = RevisionRecordForm(data=form_data, files={'photo_of_item': uploaded_image})

        self.assertTrue(form.is_valid())
class StandardPpeFormTest(BaseFormTest):

    def test_standard_ppe_form_upload(self):
        form_data = {'code': 'EN123', 'description': 'Test Standard'}

        # Assumed placeholder for the image field in StandardPpe
        uploaded_image_content = self.create_test_image()
        uploaded_image = SimpleUploadedFile("standard_image.jpg", uploaded_image_content, content_type="image/jpeg")

        form = StandardPpeForm(data=form_data, files={'image': uploaded_image})

        # Replace 'image' with the correct field name when implemented
        self.assertTrue(form.is_valid())

    def test_standard_ppe_form_missing_image(self):
        form_data = {'code': 'EN123', 'description': 'Test Standard'}

        form = StandardPpeForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors)  # Replace 'image' with correct field name


class ManufacturerFormTest(BaseFormTest):

    def test_manufacturer_form_upload(self):
        form_data = {'name': 'Sample Manufacturer'}

        # Assumed placeholder for the logo field in Manufacturer
        uploaded_image_content = self.create_test_image()
        uploaded_logo = SimpleUploadedFile("manufacturer_logo.jpg", uploaded_image_content, content_type="image/jpeg")

        form = ManufacturerForm(data=form_data, files={'logo': uploaded_logo})

        # Replace 'logo' with the correct field name when implemented
        self.assertTrue(form.is_valid())

    def test_manufacturer_form_missing_logo(self):
        form_data = {'name': 'Sample Manufacturer'}

        form = ManufacturerForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('logo', form.errors)  # Replace 'logo' with correct field name
class RevisionDataFormTest(BaseFormTest):

    def test_valid_revision_data_form(self):
        form_data = {
            'name_ppe': 'Valid PPE',
            'lifetime_of_ppe': self.lifetime_of_ppe.id,
            'type_of_ppe': self.type_of_ppe.id
        }
        uploaded_image_content = self.create_test_image()
        uploaded_image = SimpleUploadedFile("image.jpg", uploaded_image_content, content_type="image/jpeg")
        uploaded_document = SimpleUploadedFile("manual.pdf", b"dummy content", content_type="application/pdf")

        form = RevisionDataForm(data=form_data, files={
            'image_items': uploaded_image,
            'manual_for_revision': uploaded_document
        })

        self.assertTrue(form.is_valid())

    def test_revision_data_form_without_image(self):
        form_data = {
            'name_ppe': 'Missing Image PPE',
            'lifetime_of_ppe': self.lifetime_of_ppe.id,
            'type_of_ppe': self.type_of_ppe.id
        }
        uploaded_document = SimpleUploadedFile("manual.pdf", b"dummy content", content_type="application/pdf")

        form = RevisionDataForm(data=form_data, files={
            'manual_for_revision': uploaded_document
        })

        self.assertFalse(form.is_valid())
        self.assertIn('image_items', form.errors)

    def test_revision_data_form_without_document(self):
        form_data = {
            'name_ppe': 'Missing Document PPE',
            'lifetime_of_ppe': self.lifetime_of_ppe.id,
            'type_of_ppe': self.type_of_ppe.id
        }
        uploaded_image_content = self.create_test_image()
        uploaded_image = SimpleUploadedFile("image.jpg", uploaded_image_content, content_type="image/jpeg")

        form = RevisionDataForm(data=form_data, files={
            'image_items': uploaded_image
        })

        self.assertFalse(form.is_valid())
        self.assertIn('manual_for_revision', form.errors)

    def test_revision_data_form_without_image_and_document(self):
        form_data = {
            'name_ppe': 'Missing Both PPE',
            'lifetime_of_ppe': self.lifetime_of_ppe.id,
            'type_of_ppe': self.type_of_ppe.id
        }

        form = RevisionDataForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('image_items', form.errors)
        self.assertIn('manual_for_revision', form.errors)