from unittest import skip
from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase, Client

from django.urls import reverse

from django.contrib.messages import get_messages
from PIL import Image
import io
from revisions.models import *
from revisions.forms import StandardPpeForm
from accounts.models import ItemGroup, CustomUser

# Create your tests here.


"""Models"""
"""StandardPpe"""
class StandardPpeModelTest(TestCase):
    def test_string_representation(self):
        standard_ppe = StandardPpe(code='EN362', description='Test PPE')
        self.assertEqual(str(standard_ppe), 'EN362')

    def test_verbose_name(self):
        self.assertEqual(StandardPpe._meta.verbose_name, 'Standard PPE')
        self.assertEqual(StandardPpe._meta.verbose_name_plural, 'Standards PPE')

class StandardPpeTestCase(TestCase):
    def test_create_standard_ppe(self):
        standard_ppe = StandardPpe.objects.create(code="EN 362", description="Testovací popis")
        self.assertEqual(standard_ppe.code, "EN 362")
        self.assertEqual(standard_ppe.description, "Testovací popis")
        self.assertEqual(str(standard_ppe), "EN 362")

class MaterialTypeTestCase(TestCase):
    def test_create_material_type(self):
        material_type = MaterialType.objects.create(name="Ocel")
        self.assertEqual(material_type.name, "Ocel")
        self.assertEqual(str(material_type), "Ocel")


"""Manufacturer"""
class ManufacturerTestCase(TestCase):
    def setUp(self):
        self.material_type = MaterialType.objects.create(name="helmet")
        self.manufacturer = Manufacturer.objects.create(name="Petzl")
    def test_create_manufacturer(self):
        lifetime_of_ppe = LifetimeOfPpe.objects.create(
            manufacturer=self.manufacturer,
            material_type=self.material_type,
            lifetime_use_years=5,
            lifetime_manufacture_years=10
        )
        self.assertEqual(str(self.manufacturer), "Petzl")
        self.assertEqual(str(lifetime_of_ppe), "Petzl - helmet")

"""TypeOfPpe"""
class TypeOfPpeTestCase(TestCase):
    def test_create_type_of_ppe(self):
        type_of_ppe = TypeOfPpe.objects.create(
            group_type_ppe="Helma",
            price=100.00
        )
        self.assertEqual(type_of_ppe.price, 100.00)
        self.assertEqual(str(type_of_ppe), "Helma cena: 100.00 kč")


    def test_duplicate_group_type_ppe(self):
        # Původní záznam
        TypeOfPpe.objects.create(group_type_ppe='Test Type', price=100.00)

        # Pokus o vložení duplicitního záznamu
        with self.assertRaises(IntegrityError):
            TypeOfPpe.objects.create(group_type_ppe='Test Type', price=100.00)
"""RevisionData"""
class RevisionDataTestCase(TestCase):
    def setUp(self):
        self.material_type = MaterialType.objects.create(name="Textile PPE")
        self.manufacturer = Manufacturer.objects.create(name="Singing Rock")
        self.lifetime_of_ppe = LifetimeOfPpe.objects.create(
            manufacturer=self.manufacturer,
            material_type=self.material_type,
            lifetime_use_years=3,
            lifetime_manufacture_years=5
        )

        self.type_of_ppe = TypeOfPpe.objects.create(group_type_ppe="slings", price=50.00)
        self.standard_ppe = StandardPpe.objects.create(code="EN 354", description="Fasteners, Spojovací prostředky")

    def test_create_revision_data(self):
        revision_data = RevisionData.objects.create(
            lifetime_of_ppe=self.lifetime_of_ppe,  # Odkazuje na lifetime_of_ppe místo manufacturer
            group_type_ppe=self.type_of_ppe,
            name_ppe="OPEN SLING 20 mm 80cm modrá",
            notes="špatně čitelný štítek"
        )
        revision_data.standard_ppe.add(self.standard_ppe)
        self.assertIn(self.standard_ppe, revision_data.standard_ppe.all())
        self.assertEqual(str(revision_data), "OPEN SLING 20 mm 80cm modrá (slings cena: 50.00 kč) by Singing Rock")


"""RevisionRecord"""

class RevisionRecordTestCase(TestCase):

    def setUp(self):
        self.material_type = MaterialType.objects.create(name="Harness")
        self.manufacturer = Manufacturer.objects.create(name="Singing Rock")
        self.lifetime_of_ppe = LifetimeOfPpe.objects.create(
            manufacturer=self.manufacturer,
            material_type=self.material_type,
            lifetime_use_years=10,
            lifetime_manufacture_years=15
        )

        self.type_of_ppe = TypeOfPpe.objects.create(
            group_type_ppe="height work harness",
            price=180.00
        )

        # Vytvoření objektu RevisionData s lifetime_of_ppe
        self.revision_data = RevisionData.objects.create(
            lifetime_of_ppe=self.lifetime_of_ppe,
            group_type_ppe=self.type_of_ppe,
            name_ppe="expert 3D speed",
            notes="serial under speed"
        )

        self.revision_data.standard_ppe.add(
            StandardPpe.objects.create(code="EN 358, EN 361, EN 813, EN 1497", description="bla, bla, bla, bla")
        )

        self.user = CustomUser.objects.create_user(username='tester', email='tester@example.com', password='password')
        self.item_group = ItemGroup.objects.create(name="Test Group")

    def create_revision_record(self, serial_number, date_manufacture, date_of_first_use, notes="Test revision record"):
        return RevisionRecord(
            revision_data=self.revision_data,
            serial_number=serial_number,
            date_manufacture=date_manufacture,
            date_of_first_use=date_of_first_use,
            item_group=self.item_group,
            owner=self.user,
            created_by=self.user,
            notes=notes
        )

    def test_create_revision_record(self):
        revision_record = self.create_revision_record(
            "SNpositiv",
            date(2016, 2, 1),
            date(2017, 4, 9)
        )
        revision_record.save()
        print(str(revision_record))
        self.assertEqual(str(revision_record), (
            f"Singing Rock | height work harness | expert 3D speed | "
            f"SNpositiv | {revision_record.date_manufacture} | {revision_record.date_of_first_use} | "
            f"{revision_record.date_of_revision} | {revision_record.date_of_next_revision} | fit | Test revision record"
        ))

    def test_create_revision_exceeded_lifetime_first_record(self):
        revision_record = self.create_revision_record(
            "SNexpiration",
            date(2013, 2, 1),
            date(2015, 4, 9)
        )
        # Získání lifetime_of_ppe z revision_data
        lifetime_of_ppe = revision_record.revision_data.lifetime_of_ppe

        max_use_expiry = revision_record.date_of_first_use + timedelta(days=365 * lifetime_of_ppe.lifetime_use_years)
        max_manufacture_expiry = revision_record.date_manufacture + timedelta(
            days=365 * lifetime_of_ppe.lifetime_manufacture_years)
        days_until_expiry = (min(max_use_expiry, max_manufacture_expiry) - timezone.now().date()).days

        expected_full_message = f"The lifetime of this item will end in {days_until_expiry} days."
        with self.assertRaises(ValidationError) as e:
            revision_record.full_clean()

        print(str(revision_record))
        self.assertIn(expected_full_message, str(e.exception))

    def test_create_revision_exceeded_lifetime_manufactures_record(self):
        revision_record = self.create_revision_record(
            "SNexpirationManufacture",
            date(2010, 2, 1),
            date(2016, 4, 9)
        )
        # Získání lifetime_of_ppe z revision_data
        lifetime_of_ppe = revision_record.revision_data.lifetime_of_ppe

        max_use_expiry = revision_record.date_of_first_use + timedelta(days=365 * lifetime_of_ppe.lifetime_use_years)
        max_manufacture_expiry = revision_record.date_manufacture + timedelta(days=365 * lifetime_of_ppe.lifetime_manufacture_years)
        days_until_expiry = (min(max_use_expiry, max_manufacture_expiry) - timezone.now().date()).days
        expected_full_message = f"The lifetime of this item will end in {days_until_expiry} days."
        with self.assertRaises(ValidationError) as e:
            revision_record.full_clean()
        print(str(revision_record))
        self.assertIn(expected_full_message, str(e.exception))

    def test_create_revision_expire_lifetime_manufactures_record(self):
        revision_record = self.create_revision_record(
            "SNManufactureEnd",
            date(2009, 2, 1),
            date(2016, 4, 9)
        )
        expected_full_message = "The item has exceeded its lifetime from manufacture according to manufacturer guidelines."
        with self.assertRaises(ValidationError) as e:
            revision_record.full_clean()
        print(str(revision_record))
        self.assertIn(expected_full_message, str(e.exception))

    def test_auto_set_dates_on_creation(self):
        revision_record2 = self.create_revision_record(
            "SNadd_creation",
            date(2020, 10, 9),
            date(2020, 11, 1)
        )


        revision_record2.save()
        print(str(revision_record2))
        self.assertIsNotNone(revision_record2.date_of_revision)
        self.assertEqual(revision_record2.date_of_next_revision, revision_record2.date_of_revision + timedelta(days=365))

    def test_create_revision_expire_lifetime_use_record(self):
        revision_record = self.create_revision_record(
            "SNEndlifetime",
            date(2012, 2, 1),
            date(2013, 4, 9)
        )
        expected_full_message = "The item has exceeded its lifetime from the first use according to manufacturer guidelines."
        with self.assertRaises(ValidationError) as e:
            revision_record.full_clean()
        print(str(revision_record))
        self.assertIn(expected_full_message, str(e.exception))

    def test_revision_data_cannot_be_none(self):
        revision_record = RevisionRecord(
            revision_data=None,  # Intentionally set to None to trigger the error
            serial_number="SNInvalid",
            date_manufacture=date(2016, 2, 1),
            date_of_first_use=date(2016, 4, 9),
            item_group=self.item_group,
            owner=self.user,
            created_by=self.user
        )
        with self.assertRaises(ValidationError) as context:
            revision_record.full_clean()
        self.assertIn('Data revize nemohou být prázdná.', str(context.exception))
"""views.py"""

@skip
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

class RevisionRecordTest(TestCase):


    def setUp(self):
        # Nastavení uživatele pro přihlašování
        self.user = CustomUser.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')

        # Vytvoření nezbytných závislostí
        self.manufacturer = Manufacturer.objects.create(
            name='Test Manufacturer',
        )

        self.material_type = MaterialType.objects.create(
            name='Test Material Type',
        )

        self.lifetime_of_ppe = LifetimeOfPpe.objects.create(
            manufacturer=self.manufacturer,
            material_type=self.material_type,
            lifetime_use_years=10,
            lifetime_manufacture_years=10,
        )

        self.group_type_ppe = TypeOfPpe.objects.create(
            group_type_ppe='Test Group Type',
            price=100.00,
        )

        # Vytvoření příkladu RevisionData pro použití v testech
        self.revision_data = RevisionData.objects.create(
            name_ppe='Example PPE',
            lifetime_of_ppe=self.lifetime_of_ppe,
            group_type_ppe=self.group_type_ppe,
        )

    def test_create_revision_record_view(self):
        # Setup pro přístup k stránce vytvoření a kontrola inicializace stránky
        url = reverse('add_revision')  # Ujistěte se, že název URL je správný
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_form.html')
        self.assertContains(response, 'Add New Revision Data')

        # Kontrola odeslání formuláře s platnými daty
        data = {
            'revision_data': self.revision_data.id,  # Zajistěte, že tento objekt opravdu existuje
            'serial_number': '1234',
            'date_manufacture': '2023-10-12',
            'date_of_first_use': '2023-10-13',
            'owner': self.user.id,  # Nastavení vlastníka jako přihlášeného uživatele
            'verdict': 'fit',  # Použití správné volby pro verdict
            # Ostatní nezbytná pole podle definice vašeho modelu a formuláře
        }

        response = self.client.post(url, data, follow=True)  # `follow=True` znamená sledování přesměrování

        # Kontrola, zda zůstáváme na stejné URL po úspěšném odeslání
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_form.html')

        # Ověření zobrazení úspěšné zprávy při zůstatí na téže stránce
        self.assertContains(response, 'The item was successfully saved')

        # Ověření, že byl záznam úspěšně vytvořen v databázi
        self.assertTrue(RevisionRecord.objects.filter(serial_number='1234').exists())

    def test_create_revision_record_post(self):
        url = reverse('add_revision')
        data = {
            'revision_data': self.revision_data.id,
            'serial_number': '2234',
            'date_manufacture': '2023-10-12',
            'date_of_first_use': '2023-10-18',
            'owner': self.user.id,
            'verdict': 'fit',
            # Další nezbytná pole dle modelu
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Status code 302 pro úspešné přesměrování
        self.assertTrue(RevisionRecord.objects.filter(serial_number='2234').exists())

    def test_add_revision_data_button_visible(self):
        url = reverse('add_revision')
        response = self.client.get(url)
        self.assertContains(response, 'Add New Revision Data')


class RevisionDataTest(TestCase):

    def setUp(self):
        # Nastavení uživatele pro přihlašování
        self.user = CustomUser.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')

        # Vytvoření nezbytných závislostí
        self.manufacturer = Manufacturer.objects.create(
            name='Test Manufacturer',
        )
        self.material_type = MaterialType.objects.create(
            name='Test Material Type',
        )
        self.lifetime_of_ppe = LifetimeOfPpe.objects.create(
            manufacturer=self.manufacturer,
            material_type=self.material_type,
            lifetime_use_years=10,
            lifetime_manufacture_years=10,
        )
        self.group_type_ppe = TypeOfPpe.objects.create(
            group_type_ppe='Test Group Type',
            price=100.00,
        )
        self.standard_ppe_obj = StandardPpe.objects.create(
            code='EN123',
            description='Test StandardPpe',
        )

    def test_create_revision_data_view(self):
        # Ověření, že formulářová stránka je přístupná
        url = reverse('add_revision_data')  # Ujistěte se, že URL název je správný
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_form.html')

    def test_create_revision_data_post(self):
        # Vytvoření nového záznamu a kontrola přesměrování
        url = reverse('add_revision_data')
        # Vytvoření validního test image v paměti s Pillow
        image_data = io.BytesIO()
        image = Image.new('RGB', (100, 100), color=(255, 0, 0))
        image.save(image_data, format='JPEG')
        image_data.seek(0)

        test_image = SimpleUploadedFile("test_image.jpg", image_data.read(), content_type="image/jpeg")
        test_file = SimpleUploadedFile("manual.txt", b"Manual content", content_type="text/plain")

        data = {
            'name_ppe': 'New PPE',
            'lifetime_of_ppe': self.lifetime_of_ppe.id,
            'group_type_ppe': self.group_type_ppe.id,
            'standard_ppe': [self.standard_ppe_obj.id],
            'image_items': test_image,
            'manual_for_revision': test_file,
        }
        # Odeslání POST žádosti s Multipart form data
        response = self.client.post(url, data, follow=True) # follow=True sleduje přesměrování
        if response.context and response.context.get('form'):
            # Tisk chyby formuláře
            print(response.context['form'].errors)

        try:
            self.assertEqual(response.status_code, 200)
            # Ověření, že záznam byl úspěšně vytvořen
            self.assertTrue(RevisionData.objects.filter(name_ppe='New PPE').exists())
        except AssertionError as e:
            print("Test selhal:")
            print(f"Response status kód: {response.status_code}")
            print(f"Obsah odpovědi: {response.content}")
            raise e

    def test_redirect_after_creation(self):
        # Testování přesměrování na 'next' po úspěšném uložení
        url = reverse('add_revision_data') + '?next=' + reverse('add_revision')
        data = {
            'name_ppe': 'Another PPE',
            'lifetime_of_ppe': self.lifetime_of_ppe.id,
            'group_type_ppe': self.group_type_ppe.id,
            'standard_ppe':  [self.standard_ppe_obj.id],
            # Další povinná pole
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_form.html')  # Kontrola, že se přesměrovalo zpět na formulář

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

# class RevisionDataFormTest(TestCase):
#     def setUp(self):
#         self.lifetime_of_ppe = LifetimeOfPpe.objects.create(name="Life1")
#         self.group_type_ppe = TypeOfPpe.objects.create(name="Group1")
#         self.standard_ppe = StandardPpe.objects.create(name="Standard1")
#     def test_form_valid_data(self):
#         form = RevisionDataForm(data={
#
#         })


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