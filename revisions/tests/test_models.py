import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from revisions.models import *
from accounts.models import CustomUser
import datetime

class RevisionsModelsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Vytvoření základních údajů pro testování modelů
        cls.material_image = SimpleUploadedFile(
            "material_image.jpg",
            content=b"material_image_content",
            content_type="image/jpeg"
        )
        cls.material_type = MaterialType.objects.create(
            name='Textil',
            symbol=cls.material_image
        )

        cls.standard_image = SimpleUploadedFile(
            "standard_image.jpg",
            content=b"standard_image_content",
            content_type="image/jpeg"
        )
        cls.standard_ppe = StandardPpe.objects.create(
            code='EN 362',
            description='Norma pro spojovací prostředky',
            image=cls.standard_image
        )

        cls.manufacturer_logo = SimpleUploadedFile(
            "manufacturer_logo.jpg",
            content=b"manufacturer_logo_content",
            content_type="image/jpeg"
        )
        cls.manufacturer = Manufacturer.objects.create(
            name='Singing Rock',
            logo=cls.manufacturer_logo
        )

        cls.lifetime_of_ppe = LifetimeOfPpe.objects.create(
            manufacturer=cls.manufacturer,
            material_type=cls.material_type,
            lifetime_use_years=10,
            lifetime_manufacture_years=15
        )

        cls.type_of_ppe_image = SimpleUploadedFile(
            "type_of_ppe_image.jpg",
            content=b"type_of_ppe_image_content",
            content_type="image/jpeg"
        )
        cls.type_of_ppe = TypeOfPpe.objects.create(
            group_type_ppe='Helma',
            price=100.00,
            image=cls.type_of_ppe_image
        )

        cls.revision_data_image = SimpleUploadedFile(
            "revision_data_image.jpg",
            content=b"revision_data_image_content",
            content_type="image/jpeg"
        )
        cls.revision_data = RevisionData.objects.create(
            image_items=cls.revision_data_image,
            lifetime_of_ppe=cls.lifetime_of_ppe,
            group_type_ppe=cls.type_of_ppe,
            name_ppe='Flash industry',
            manual_for_revision='manual.pdf'
        )
        cls.revision_data.standard_ppe.add(cls.standard_ppe)

        cls.revision_record_image = SimpleUploadedFile(
            "revision_record_image.jpg",
            content=b"revision_record_image_content",
            content_type="image/jpeg"
        )

        cls.user = CustomUser.objects.create(username='testuser', password='testpass')
        cls.revision_record = RevisionRecord.objects.create(
            revision_data=cls.revision_data,
            serial_number='SN12345',
            date_manufacture=datetime.date(2020, 1, 1),
            owner=cls.user,
            photo_of_item=cls.revision_record_image,
            verdict='fit',
            created_by=cls.user,
        )

    def test_material_type_creation(self):
        self.assertEqual(self.material_type.name, 'Textil')

    def test_material_type_image_upload(self):
        self.assertTrue(self.material_type.symbol.name.startswith('static/image/material/material_image'))

    def test_standard_ppe_creation(self):
        self.assertEqual(self.standard_ppe.code, 'EN 362')
        self.assertEqual(self.standard_ppe.description, 'Norma pro spojovací prostředky')

    def test_standard_ppe_image_upload(self):
        self.assertTrue(self.standard_ppe.image.name.startswith('static/image/standard_ppe/logo/standard_image'))

    def test_manufacturer_creation(self):
        self.assertEqual(self.manufacturer.name, 'Singing Rock')

    def test_manufacturer_logo_upload(self):
        self.assertTrue(self.manufacturer.logo.name.startswith('static/image/manufacturer/logo/manufacturer_logo'))

    def test_lifetime_of_ppe_creation(self):
        self.assertEqual(self.lifetime_of_ppe.lifetime_use_years, 10)
        self.assertEqual(self.lifetime_of_ppe.lifetime_manufacture_years, 15)

    def test_type_of_ppe_image_upload(self):
        self.assertTrue(self.type_of_ppe.image.name.startswith('static/image/type_of_ppe/type_of_ppe_image'))

    def test_type_of_ppe_creation(self):
        self.assertEqual(self.type_of_ppe.group_type_ppe, 'Helma')
        self.assertEqual(self.type_of_ppe.price, 100.00)

    def test_revision_data_creation(self):
        self.assertEqual(self.revision_data.name_ppe, 'Flash industry')
        self.assertTrue(self.revision_data.standard_ppe.filter(pk=self.standard_ppe.pk).exists())

    def test_revision_data_image_upload(self):
        self.assertTrue(self.revision_data.image_items.name.startswith('static/image/revision_data/revision_data_image'))

    def test_revision_record_creation(self):
        self.assertEqual(self.revision_record.serial_number, 'SN12345')
        self.assertEqual(self.revision_record.verdict, 'fit')

    def test_revision_record_image_upload(self):
        self.assertTrue(self.revision_record.photo_of_item.name.startswith('media/image/revision_record/revision_record_image'))

    @classmethod
    def tearDownClass(cls):
        # Odebereme všechny obrázky, které byly nahrané během testů
        cls._remove_test_file(cls.material_type.symbol.path)
        cls._remove_test_file(cls.standard_ppe.image.path)
        cls._remove_test_file(cls.manufacturer.logo.path)
        cls._remove_test_file(cls.type_of_ppe.image.path)
        cls._remove_test_file(cls.revision_data.image_items.path)
        cls._remove_test_file(cls.revision_record.photo_of_item.path)
        super().tearDownClass()

    @staticmethod
    def _remove_test_file(path):
        if os.path.isfile(path):
            os.remove(path)