from datetime import date
from unittest import skip

from django.db.models import ProtectedError
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from accounts import urls
from revisions.models import *

User = get_user_model()

class BaseViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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
        cls.revision_data_image = SimpleUploadedFile(
            "revision_data_image.jpg",
            content=b"revision_data_image_content",
            content_type="image/jpeg"
        )
        cls.revision_data = RevisionData.objects.create(
            image_items=cls.revision_data_image,
            lifetime_of_ppe=cls.lifetime_of_ppe,
            group_type_ppe=cls.type_of_ppe,
            name_ppe='Test PPE',
        )
        cls.revision_data.standard_ppe.add(cls.standard_ppe)

    def setUp(self):
        self.client.login(username='testuser', password='testpass')

### Dědění ze základní třídy:


class StandardPpeViewsTest(BaseViewsTest):

    def test_add_standard_ppe_view_get(self):
        url = reverse('add_standard_ppe')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_form.html')

    def test_add_standard_ppe_view_post_valid(self):
        url = reverse('add_standard_ppe')
        data = {'code': 'EN124', 'description': 'New Standard'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(StandardPpe.objects.filter(code='EN124').exists())

    def test_add_standard_ppe_view_post_invalid(self):
        url = reverse('add_standard_ppe')
        data = {'code': '', 'description': 'Invalid Standard'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('code', form.errors)

    def test_access_to_add_standard_ppe_without_login(self):
        self.client.logout()
        response = self.client.get(reverse('add_standard_ppe'))
        login_url = f"{reverse('login')}?next={reverse('add_standard_ppe')}"
        self.assertRedirects(response, login_url)


class ManufacturerViewsTest(BaseViewsTest):
    def get_and_assert_template(self, url_name, template_name, args=None):
        url = reverse(url_name, args=args)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        return response

    def post_and_assert_redirect(self, url_name, data, args=None):
        url = reverse(url_name, args=args)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        return response

    def assert_form_invalid(self, url_name, data, expected_field_error, args=None):
       url = reverse(url_name, args=args)
       response = self.client.post(url, data)
       self.assertEqual(response.status_code, 200)
       form = response.context['form']
       self.assertFalse(form.is_valid())
       self.assertIn(expected_field_error, form.errors)

    def access_requires_login(self, url_name):
        self.client.logout()
        response = self.client.get(reverse(url_name))
        login_url = f"{reverse('login')}?next={reverse(url_name)}"
        self.assertRedirects(response, login_url)

    def test_add_manufacturer_view_get(self):
        self.get_and_assert_template('add_manufacturer', 'revision_form.html')

    def test_add_manufacturer_view_post_valid(self):
        data = {'name': 'New Manufacturer'}
        self.post_and_assert_redirect('add_manufacturer', data)
        self.assertTrue(Manufacturer.objects.filter(name='New Manufacturer').exists())

    def test_add_manufacturer_view_post_invalid(self):
        data = {'name': ''}  # Neplatné prázdné jméno výrobce
        self.assert_form_invalid('add_manufacturer', data, 'name')

    def test_access_to_add_manufacturer_without_login(self):
        self.access_requires_login('add_manufacturer')

    def test_edit_manufacturer_view_get(self):
        self.get_and_assert_template('edit_manufacturer', 'revision_form.html', args=[self.manufacturer.pk])

    def test_edit_manufacturer_view_post_valid(self):
        data = {'name': 'Updated Manufacturer'}
        self.post_and_assert_redirect('edit_manufacturer', data, args=[self.manufacturer.pk])
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, 'Updated Manufacturer')

    def test_edit_manufacturer_view_post_invalid(self):
        data = {'name': ''}  # Neplatné prázdné jméno
        self.assert_form_invalid('edit_manufacturer', data, 'name', args=[self.manufacturer.pk])
    @skip
    def test_delete_manufacturer_view_with_linked_lifetime_of_ppe(self):
        # URL pro odstranění konkrétního výrobce
        url = reverse('delete_manufacturer', args=[self.manufacturer.id])

        # Odeslání POST požadavku pro odstranění
        response = self.client.post(url)

        # Ověření, že status kód je 200, což znamená, že byl formulář správně zobrazen
        self.assertEqual(response.status_code, 200)

        # Ověření, že šablona 'confirm_delete.html' byla použita
        self.assertTemplateUsed(response, 'confirm_delete.html')

        # Ověření, že chybová zpráva je správně zobrazená
        self.assertContains(response, "Cannot delete manufacturer because it is referenced by lifetime records.")

        # Ověření, že Manufacturer stále existuje (nebyl smazán)
        self.assertTrue(Manufacturer.objects.filter(id=self.manufacturer.id).exists())

class LifetimeOfPpeViewsTest(BaseViewsTest):

    # Pomocná metoda k otestování GET požadavku a šablony
    def get_and_assert_template(self, url_name, template_name):
        response = self.client.get(reverse(url_name))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)

    # Pomocná metoda pro odeslání POST požadavku a kontrolu přesměrování
    def post_and_assert_redirect(self, url_name, data,args=None):
        url = reverse(url_name, args=args)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        return response

    # Pomocná metoda pro kontrolu, že je formulář neplatný
    def assert_form_invalid(self, url_name, data, expected_field_error, args=None):
        url = reverse(url_name, args=args)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn(expected_field_error, form.errors)

    # Pomocná metoda pro validaci vyžadovaného přihlášení
    def access_requires_login(self, url_name):
        self.client.logout()
        response = self.client.get(reverse(url_name))
        login_url = f"{reverse('login')}?next={reverse(url_name)}"
        self.assertRedirects(response, login_url)

    # Test GET požadavku na přidání Lifetime of PPE
    def test_add_lifetime_of_ppe_view_get(self):
        self.get_and_assert_template('add_lifetime_of_ppe', 'revision_form.html')

    # Test POST požadavku s validními daty
    def test_add_lifetime_of_ppe_view_post_valid(self):
        data = {
            'manufacturer': self.manufacturer.id,
            'material_type': self.material_type.id,
            'lifetime_use_years': 5,
            'lifetime_manufacture_years': 10
        }
        response = self.client.post(reverse('add_lifetime_of_ppe'), data)

        # Pokud status kód není 302, znamená to, že formulář má chyby
        if response.status_code != 302:
            form = response.context['form']
            print(form.errors)  # Tiskne chyby formuláře do konzole pro ladění

        self.assertEqual(response.status_code, 302)
        self.assertTrue(LifetimeOfPpe.objects.filter(lifetime_use_years=5).exists())

    # Test POST požadavku s neplatnými daty
    def test_add_lifetime_of_ppe_view_post_invalid(self):
        data = {
            'manufacturer': '',
            'material_type': self.material_type.id,
            'lifetime_use_years': 5,
            'lifetime_manufacture_years': 10
        }
        self.assert_form_invalid('add_lifetime_of_ppe', data, 'manufacturer')

    # Ověření přístupu bez přihlášení
    def test_access_to_add_lifetime_of_ppe_without_login(self):
        self.access_requires_login('add_lifetime_of_ppe')

    # Test pro GET úpravu Lifetime of PPE
    def test_edit_lifetime_of_ppe_view_get(self):
        url = reverse('edit_lifetime_of_ppe', args=[self.lifetime_of_ppe.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_form.html')

    # Test pro POST úpravu Lifetime of PPE s validními daty
    def test_edit_lifetime_of_ppe_view_post_valid(self):
        data = {
            'manufacturer': self.manufacturer.id,
            'material_type': self.material_type.id,
            'lifetime_use_years': 6,
            'lifetime_manufacture_years': 12
        }
        self.post_and_assert_redirect('edit_lifetime_of_ppe', data, args=[self.lifetime_of_ppe.id])
        self.lifetime_of_ppe.refresh_from_db()
        self.assertEqual(self.lifetime_of_ppe.lifetime_use_years, 6)

    # Test pro POST úpravu s neplatnými daty
    def test_edit_lifetime_of_ppe_view_post_invalid(self):
        data = {
            'manufacturer': '',  # Neplatné prázdné ID výrobce
            'material_type': self.material_type.id,
            'lifetime_use_years': 6,
            'lifetime_manufacture_years': 12
        }
        self.assert_form_invalid('edit_lifetime_of_ppe', data, 'manufacturer', args=[self.lifetime_of_ppe.id])
    # Test pro smazání Lifetime of PPE
    def test_delete_lifetime_of_ppe_protected(self):
        url = reverse('delete_lifetime_of_ppe', args=[self.lifetime_of_ppe.id])
        # Očekáváme, že požadavek vyvolá výjimku kvůli ochraně dat
        with self.assertRaises(ProtectedError):
            self.client.post(url)
        # Ověřujeme, že LifetimeOfPpe stále existuje v databázi
        self.assertTrue(LifetimeOfPpe.objects.filter(id=self.lifetime_of_ppe.id).exists())

class TypeOfPpeViewsTest(BaseViewsTest):

    # Test GET požadavku na přidání Type of PPE
    def test_add_type_of_ppe_view_get(self):
        url = reverse('add_type_of_ppe')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'type_of_ppe_form.html')  # Ujistěte se, že tato šablona existuje

    # Test POST požadavku s validními daty
    def test_add_type_of_ppe_view_post_valid(self):
        data = {'group_type_ppe': 'New Group', 'price': 150.00}
        response = self.client.post(reverse('add_type_of_ppe'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TypeOfPpe.objects.filter(group_type_ppe='New Group').exists())

    # Test POST požadavku s neplatnými daty
    def test_add_type_of_ppe_view_post_invalid(self):
        data = {'group_type_ppe': '', 'price': 150.00}  # Neplatné prázdné jméno skupiny
        response = self.client.post(reverse('add_type_of_ppe'), data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('group_type_ppe', form.errors)

    # Test pro přístup bez přihlášení
    def test_access_to_add_type_of_ppe_without_login(self):
        self.client.logout()
        response = self.client.get(reverse('add_type_of_ppe'))
        login_url = f"{reverse('login')}?next={reverse('add_type_of_ppe')}"
        self.assertRedirects(response, login_url)

    # Test pro GET úpravu Type of PPE
    def test_edit_type_of_ppe_view_get(self):
        url = reverse('edit_type_of_ppe', args=[self.type_of_ppe.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'type_of_ppe_form.html')

    # Test pro POST úpravu Type of PPE s validními daty
    def test_edit_type_of_ppe_view_post_valid(self):
        url = reverse('edit_type_of_ppe', args=[self.type_of_ppe.id])
        data = {'group_type_ppe': 'Updated Group', 'price': 200.00}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.type_of_ppe.refresh_from_db()
        self.assertEqual(self.type_of_ppe.group_type_ppe, 'Updated Group')
        self.assertEqual(self.type_of_ppe.price, 200.00)

    # Test pro POST úpravu s neplatnými daty
    def test_edit_type_of_ppe_view_post_invalid(self):
        url = reverse('edit_type_of_ppe', args=[self.type_of_ppe.id])
        data = {'group_type_ppe': '', 'price': 200.00}  # Neplatné prázdné jméno skupiny
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('group_type_ppe', form.errors)

    # Test pro odstranění Type of PPE
    def test_delete_type_of_ppe_view(self):
        url = reverse('delete_type_of_ppe', args=[self.type_of_ppe.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TypeOfPpe.objects.filter(id=self.type_of_ppe.id).exists())

class RevisionDataViewsTest(BaseViewsTest):

    def test_add_revision_data_view_get(self):
        url = reverse('add_revision_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_form.html')

    def test_add_revision_data_view_post_valid(self):
        url = reverse('add_revision_data')
        uploaded_image = SimpleUploadedFile("test_image.jpg", b"test_image_content", content_type="image/jpeg")
        uploaded_manual = SimpleUploadedFile("manual.txt", b"manual content", content_type="text/plain")
        data = {
            'name_ppe': 'New PPE Valid',
            'lifetime_of_ppe': self.lifetime_of_ppe.id,
            'group_type_ppe': self.type_of_ppe.id,
            'standard_ppe': [self.standard_ppe.id],
            'image_items': uploaded_image,
            'manual_for_revision': uploaded_manual
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Očekáváme, že zůstane na stejně stránce
        self.assertContains(response, "Item successfully uploaded.")  # Ověříme, zda je zpráva k dispozici
        self.assertTrue(RevisionData.objects.filter(name_ppe='New PPE Valid').exists())

    def test_add_revision_data_view_post_invalid(self):
        url = reverse('add_revision_data')
        data = {
            'name_ppe': '',  # Neplatný prázdný název
            'lifetime_of_ppe': self.lifetime_of_ppe.id,
            'group_type_ppe': self.type_of_ppe.id,
            'standard_ppe': [self.standard_ppe.id],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('name_ppe', form.errors)

    def test_access_to_add_revision_data_without_login(self):
        self.client.logout()
        response = self.client.get(reverse('add_revision_data'))
        login_url = f"{reverse('login')}?next={reverse('add_revision_data')}"
        self.assertRedirects(response, login_url)

    def test_edit_revision_data_view_get(self):
        url = reverse('edit_revision_data', args=[self.revision_data.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_form.html')

    def test_edit_revision_data_view_post_valid(self):
        url = reverse('edit_revision_data', args=[self.revision_data.id])

        with open(self.revision_data.image_items.path, 'rb') as image_file, \
                open(self.revision_data.manual_for_revision.path, 'rb') as manual_file:
            uploaded_image = SimpleUploadedFile(
                os.path.basename(image_file.name),
                image_file.read(),
                content_type='image/jpeg'
            )

            uploaded_manual = SimpleUploadedFile(
                os.path.basename(manual_file.name),
                manual_file.read(),
                content_type='text/plain'
            )

            data = {
                'name_ppe': 'Updated PPE',
                'lifetime_of_ppe': self.lifetime_of_ppe.id,
                'group_type_ppe': self.type_of_ppe.id,
                'standard_ppe': [self.standard_ppe.id],
                'image_items': uploaded_image,
                'manual_for_revision': uploaded_manual
            }

            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 302)

            self.revision_data.refresh_from_db()
            self.assertEqual(self.revision_data.name_ppe, 'Updated PPE')

    def test_edit_revision_data_view_post_invalid(self):
        url = reverse('edit_revision_data', args=[self.revision_data.id])
        data = {
            'name_ppe': '',  # Neplatný prázdný název
            'lifetime_of_ppe': self.lifetime_of_ppe.id,
            'group_type_ppe': self.type_of_ppe.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('name_ppe', form.errors)

    def test_revision_data_detail_view(self):
        url = reverse('revision_data_detail', args=[self.revision_data.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_data_detail.html')  # Ujistěte se, že tato šablona existuje
        self.assertContains(response, self.revision_data.name_ppe)

    def test_delete_revision_data_view(self):
        url = reverse('delete_revision_data', args=[self.revision_data.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(RevisionData.objects.filter(id=self.revision_data.id).exists())

class RevisionRecordViewsTest(BaseViewsTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        photo = SimpleUploadedFile("test_photo.jpg", b"test_photo_content", content_type="image/jpeg")
        cls.revision_record = RevisionRecord.objects.create(
            revision_data=cls.revision_data,
            serial_number='SN12345',
            date_manufacture=date.today(),
            date_of_first_use=date.today(),
            owner=cls.user,
            verdict='fit',
            created_by=cls.user,
            photo_of_item=photo
        )

    def get_and_assert_template(self, url_name, template_name, args=None):
        url = reverse(url_name, args=args)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        return response

    def post_and_assert_redirect(self, url_name, data, args=None):
        url = reverse(url_name, args=args)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        return response

    def assert_form_invalid(self, url_name, data, expected_field_error, args=None):
        url = reverse(url_name, args=args)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn(expected_field_error, form.errors)

    def test_create_revision_record_view_get(self):
        self.get_and_assert_template('add_revision_record', 'revision_form.html')

    def test_create_revision_record_view_post_valid(self):
        url = reverse('add_revision_record')
        photo = SimpleUploadedFile("test_photo.jpg", b"test_photo_content", content_type="image/jpeg")
        data = {
            'revision_data': self.revision_data.id,
            'serial_number': 'SN12346',
            'date_manufacture': date.today(),
            'date_of_first_use': date.today(),
            'owner': self.user.id,
            'verdict': 'fit',
            'photo_of_item': photo
        }

        response = self.client.post(url, data)

        # Kontrola, že se po úspěšném uložení zůstane na stejném URL
        self.assertEqual(response.status_code, 200)

        # Ověření, že úspěšná zpráva je správně obsahována na stránce
        self.assertContains(response, "The item was successfully saved")

        # Ověření, že nový záznam byl vytvořen
        self.assertTrue(RevisionRecord.objects.filter(serial_number='SN12346').exists())

    def test_create_revision_record_view_post_invalid(self):
        data = {
            'revision_data': self.revision_data.id,
            'serial_number': '',  # Neplatný prázdný sériový číslo
            'date_manufacture': date.today(),
            'owner': self.user.id,
            'verdict': 'fit',
        }
        self.assert_form_invalid('add_revision_record', data, 'serial_number')

    def test_access_to_create_revision_record_without_login(self):
        self.client.logout()
        response = self.client.get(reverse('add_revision_record'))
        login_url = f"{reverse('login')}?next={reverse('add_revision_record')}"
        self.assertRedirects(response, login_url)

    def test_edit_revision_record_view_get(self):
        self.get_and_assert_template('edit_revision_record', 'revision_form.html', args=[self.revision_record.id])

    def test_edit_revision_record_view_post_valid(self):
        data = {
            'revision_data': self.revision_data.id,
            'serial_number': 'SNupdated',
            'date_manufacture': date.today(),
            'date_of_first_use': date.today(),
            'owner': self.user.id,
            'verdict': 'fit',
            'photo_of_item': self.revision_record.photo_of_item
        }
        self.post_and_assert_redirect('edit_revision_record', data, args=[self.revision_record.id])
        self.revision_record.refresh_from_db()
        self.assertEqual(self.revision_record.serial_number, 'SNupdated')

    def test_edit_revision_record_view_post_invalid(self):
        data = {
            'revision_data': self.revision_data.id,
            'serial_number': '',  # Neplatný prázdný sériový číslo
            'date_manufacture': date.today(),
            'owner': self.user.id,
            'verdict': 'fit',
        }
        self.assert_form_invalid('edit_revision_record', data, 'serial_number', args=[self.revision_record.id])

    def test_revision_record_detail_view(self):
        response = self.get_and_assert_template('revision_record_detail', 'revision_record_detail.html', args=[self.revision_record.id])
        self.assertContains(response, self.revision_record.serial_number)

    def test_delete_revision_record_view(self):
        self.post_and_assert_redirect('delete_revision_record', {}, args=[self.revision_record.id])
        self.assertFalse(RevisionRecord.objects.filter(id=self.revision_record.id).exists())