from datetime import date

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from accounts.forms import CustomUser
from .models import *
from .forms import StandardPpeForm

# Create your tests here.


"""Models"""
# python manage.py test revisions.tests

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



class ManufacturerTestCase(TestCase):
    def setUp(self):
        self.material_type = MaterialType.objects.create(name="helmet")

    def test_create_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Petzl",
            material_type=self.material_type,
            lifetime_use_years=5,
            lifetime_manufacture_years=10
        )
        self.assertEqual(str(manufacturer), "Petzl - helmet")

class TypeOfPpeTestCase(TestCase):
    def test_create_type_of_ppe(self):
        type_of_ppe = TypeOfPpe.objects.create(
            group_type_ppe="Helma",
            price=100.00
        )
        self.assertEqual(type_of_ppe.price, 100.00)
        self.assertEqual(str(type_of_ppe), "Helma cena: 100.00 kč")

class RevisionDataTestCase(TestCase):
    def setUp(self):
        self.material_type = MaterialType.objects.create(name="Textile PPE")
        self.manufacturer = Manufacturer.objects.create(
            name="Singing Rock",
            material_type=self.material_type,
            lifetime_use_years=3,
            lifetime_manufacture_years=5
        )
        self.type_of_ppe = TypeOfPpe.objects.create(group_type_ppe="slings", price=50.00)
        self.standard_ppe = StandardPpe.objects.create(code="EN 354", description="Fasteners, Spojovací prostředky")

    def test_create_revision_data(self):
        revision_data = RevisionData.objects.create(
            manufacturer=self.manufacturer,
            group_type_ppe=self.type_of_ppe,
            name_ppe="OPEN SLING 20 mm 80cm modrá",
            notes="špatně čitelný štítek"
        )
        revision_data.standard_ppe.add(self.standard_ppe)
        self.assertIn(self.standard_ppe, revision_data.standard_ppe.all())
        self.assertEqual(str(revision_data), "OPEN SLING 20 mm 80cm modrá (slings cena: 50.00 kč) by Singing Rock")

class RevisionRecord(TestCase):
    def setUp(self):
        User = get_user_model()
        # Vytvoříme potřebná data pro vytvoření RevisionRecord
        self.material_type = MaterialType.objects.create(name="Harness")
        self.manufacturer = Manufacturer.objects.create(
            name="Petzl",
            material_type=self.material_type,
            lifetime_use_years=10,
            lifetime_manufacture_years=10
        )
        self.type_of_ppe = TypeOfPpe.objects.create(
            group_type_ppe="height_work_harness ",
            price=180.00
        )
        self.revision_data = RevisionData.objects.create(
            manufacturer=self.manufacturer,
            group_type_ppe=self.type_of_ppe,
            name_ppe="expert 3D speed",
            notes="serial under speed"
        )
        self.revision_data.standard_ppe.add(StandardPpe.objects.create(code="EN 358, EN 361, EN 813, EN 1497 ", description="bla, bla, bla, bla"))
        self.user = User.objects.create_user(username='tester', email='tester@example.com', password='password')
        self.item_group = ItemGroup.objects.create(name="Test Group")

    def test_create_revision_record(self):
        revision_record = RevisionRecord.objects.create(
            revision_data=self.revision_data,
            serial_number="SN123456",
            date_manufacture=date.today(),
            date_of_first_use=date.today(),
            item_group=self.item_group,
            owner=self.user,
            created_by=self.user,
            verdict=RevisionRecord.VERDICT_NEW,
            notes="Test revision record"
        )
        self.assertEqual(str(revision_record), (
            f"petzl | height_work_harness | Safety Helmet | "
            f"SN123456 | {revision_record.date_manufacture} | {revision_record.date_of_first_use} | "
            f"{revision_record.date_of_revision} | {revision_record.date_of_next_revision} | new | Test revision record"
        ))

    def test_auto_set_dates_on_creation(self):
        revision_record = RevisionRecord.objects.create(
            revision_data=self.revision_data,
            serial_number="SN789012",
            date_manufacture=date.today(),
            date_of_first_use=date.today(),
            item_group=self.item_group,
            owner=self.user,
            created_by=self.user,
            verdict=RevisionRecord.VERDICT_NEW,
            notes="Auto date test"
        )
        # Přidejte automatické ověření dat
        self.assertIsNotNone(revision_record.date_of_revision)
        self.assertEqual(revision_record.date_of_next_revision, revision_record.date_of_revision + timedelta(days=365))

    def test_revision_data_cannot_be_none(self):
        with self.assertRaises(ValueError):
            RevisionRecord.objects.create(
                revision_data=None,
                serial_number="SNInvalid",
                date_manufacture=date.today(),
                date_of_first_use=date.today(),
                created_by=self.user
            )



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