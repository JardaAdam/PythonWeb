from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from config.test_base_view import BaseViewsTest
from revisions.models import *


class StandardPpeViewsTest(BaseViewsTest):
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

    def access_requires_login(self, url_name):
        self.client.logout()
        response = self.client.get(reverse(url_name))
        login_url = f"{reverse('login')}?next={reverse(url_name)}"
        self.assertRedirects(response, login_url)

    def test_add_standard_ppe_view_get(self):
        url = reverse('add_standard_ppe')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_form.html')

    def test_add_standard_ppe_view_post_valid(self):
        url = reverse('add_standard_ppe')
        uploaded_image_ppe = SimpleUploadedFile(
            "logo.jpg", self.create_test_image(), content_type='image/jpeg')
        data = {'code': 'EN124', 'description': 'New Standard', 'image': uploaded_image_ppe}
        response = self.client.post(url, data, format='multipart')
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

    def test_edit_standard_ppe_view_get(self):
        std_ppe = StandardPpe.objects.create(code='EN125', description='Existing Standard')
        self.get_and_assert_template('edit_standard_ppe', 'revision_form.html', args=[std_ppe.pk])

    def test_edit_standard_ppe_view_post_valid(self):
        image_content = self.create_test_image()
        uploaded_image_ppe = SimpleUploadedFile(
            "test_image.jpg", image_content, content_type="image/jpeg"
        )
        std_ppe = StandardPpe.objects.create(code='EN125', description='Existing Standard', image=uploaded_image_ppe)
        new_uploaded_image = SimpleUploadedFile(
            "new_test_image.jpg", image_content, content_type="image/jpeg"
        )
        data = {'code': 'EN126', 'description': 'Updated Standard', 'image': new_uploaded_image}

        # Spuštění testu pro funkci editace
        self.post_and_assert_redirect('edit_standard_ppe', data, args=[std_ppe.pk])

        # Ověření, že data byla správně aktualizována
        std_ppe.refresh_from_db()
        self.assertEqual(std_ppe.code, 'EN126')

    def test_edit_standard_ppe_view_post_invalid(self):
        std_ppe = StandardPpe.objects.create(code='EN125', description='Existing Standard')
        data = {'code': '', 'description': 'Updated Standard'}
        self.assert_form_invalid('edit_standard_ppe', data, 'code', args=[std_ppe.pk])

    def test_delete_standard_ppe_view(self):
        std_ppe = StandardPpe.objects.create(code='EN125', description='Existing Standard')
        self.post_and_assert_redirect('delete_standard_ppe', {}, args=[std_ppe.pk])
        self.assertFalse(StandardPpe.objects.filter(id=std_ppe.id).exists())

    def test_standard_ppe_detail_view(self):
        std_ppe = StandardPpe.objects.create(code='EN125', description='Existing Standard')
        response = self.get_and_assert_template('standard_ppe_detail', 'standard_ppe_detail.html', args=[std_ppe.pk])
        self.assertContains(response, std_ppe.code)

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



    def access_requires_login(self, url_name):
        self.client.logout()
        response = self.client.get(reverse(url_name))
        login_url = f"{reverse('login')}?next={reverse(url_name)}"
        self.assertRedirects(response, login_url)

    def test_add_manufacturer_view_get(self):
        self.get_and_assert_template('add_manufacturer', 'revision_form.html')

    def test_add_manufacturer_view_post_valid(self):
        uploaded_logo = SimpleUploadedFile(
            "manufacturer_logo.jpg", self.create_test_image(), content_type='image/jpeg')
        data = {'name': 'New Manufacturer', 'logo': uploaded_logo}
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
        image_content = self.create_test_image()
        uploaded_image_ppe = SimpleUploadedFile(
            "test_image.jpg", image_content, content_type="image/jpeg"
        )
        data = {'name': 'Updated Manufacturer', 'logo': uploaded_image_ppe}
        self.post_and_assert_redirect('edit_manufacturer', data, args=[self.manufacturer.pk])
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, 'Updated Manufacturer')

    def test_edit_manufacturer_view_post_invalid(self):
        data = {'name': ''}  # Neplatné prázdné jméno
        self.assert_form_invalid('edit_manufacturer', data, 'name', args=[self.manufacturer.pk])

    def test_delete_manufacturer_view_with_linked_lifetime_of_ppe(self):
        # URL pro odstranění konkrétního výrobce
        url = reverse('delete_manufacturer', args=[self.manufacturer.id])

        # Odeslání POST požadavku pro odstranění a sledování přesměrování
        response = self.client.post(url, follow=True)

        # Ověření, že se objevila správná chybová zpráva
        self.assertContains(response, 'This item cannot be deleted because it is protected and has associated records.')

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
        manufacturer = Manufacturer.objects.create(name='Unique Manufacturer')
        material_type = MaterialType.objects.create(name='Unique Material Type')

        data = {
            'manufacturer': manufacturer.id,
            'material_type': material_type.id,
            'lifetime_use_years': 5,
            'lifetime_manufacture_years': 10
        }
        url = reverse('add_lifetime_of_ppe')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


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
        # URL pro odstranění konkrétního záznamu LifetimeOfPpe
        url = reverse('delete_lifetime_of_ppe', args=[self.lifetime_of_ppe.id])

        # Odeslání POST požadavku pro odstranění a sledování přesměrování
        response = self.client.post(url, follow=True)

        # Ověření, že se objevila správná chybová zpráva
        self.assertContains(response, 'This item cannot be deleted because it is protected and has associated records.')

        # Ověření, že Manufacturer stále existuje (nebyl smazán)
        self.assertTrue(LifetimeOfPpe.objects.filter(id=self.manufacturer.id).exists())

class TypeOfPpeViewsTest(BaseViewsTest):

    # Test GET požadavku na přidání Type of PPE
    def test_add_type_of_ppe_view_get(self):
        url = reverse('add_type_of_ppe')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_form.html')  # Ujistěte se, že tato šablona existuje

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
        self.assertTemplateUsed(response, 'revision_form.html')

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
        # Odeslání POST požadavku pro odstranění a sledování přesměrování
        response = self.client.post(url, follow=True)

        # Ověření, že se objevila správná chybová zpráva
        self.assertContains(response, 'This item cannot be deleted because it is protected and has associated records.')

        # Ověření, že Manufacturer stále existuje (nebyl smazán)
        self.assertTrue(Manufacturer.objects.filter(id=self.manufacturer.id).exists())

class RevisionDataViewsTest(BaseViewsTest):

    def test_add_revision_data_view_get(self):
        url = reverse('add_revision_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revision_form.html')

    def test_add_revision_data_view_post_valid(self):
        url = reverse('add_revision_data')
        uploaded_image_content = self.create_test_image()
        uploaded_image = SimpleUploadedFile(
            "image2.jpg", uploaded_image_content, content_type='image/jpeg'
        )
        data = {
            'name_ppe': 'Valid PPE',
            'lifetime_of_ppe': self.lifetime_of_ppe.id,
            'type_of_ppe': self.type_of_ppe.id,
            'standard_ppe': [self.standard_ppe.id],
            'image_items': uploaded_image,
            'manual_for_revision': SimpleUploadedFile("manual.pdf", b"dummy content", content_type='application/pdf')
        }
        response = self.client.post(url, data, follow=True)

        # Check HTTP response status
        self.assertEqual(response.status_code, 200)

        # Check messages
        messages = [msg for msg in response.context['messages']]
        self.assertEqual(str(messages[0]), 'The item was successfully saved from CreateMixin')

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

#open(self.revision_data.image_items.path, 'rb') as image_file, \

    def test_edit_revision_data_view_post_valid(self):
        image_content = self.create_test_image()
        uploaded_image = SimpleUploadedFile(
            "test_image.jpg", image_content, content_type="image/jpeg"
        )
        uploaded_document = SimpleUploadedFile("manual.pdf", b"dummy content", content_type="application/pdf")
        url = reverse('edit_revision_data', args=[self.revision_data.id])


        data = {
            'name_ppe': 'Updated PPE',
            'lifetime_of_ppe': self.lifetime_of_ppe.id,
            'type_of_ppe': self.type_of_ppe.id,
            'standard_ppe': [self.standard_ppe.id],
            'image_items': uploaded_image,
            'manual_for_revision': uploaded_document
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The changes have been successfully uploaded from UpdateMixin')

        # Kontrola zaktualizovaných dat
        self.revision_data.refresh_from_db()
        self.assertEqual(self.revision_data.name_ppe, 'Updated PPE')

    def test_edit_revision_data_view_post_invalid(self):
        url = reverse('edit_revision_data', args=[self.revision_data.id])
        data = {
            'name_ppe': '',  # Neplatný prázdný název
            'lifetime_of_ppe': self.lifetime_of_ppe.id,
            'type_of_ppe': self.type_of_ppe.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('name_ppe', form.errors)
        self.assertTemplateUsed(response, 'revision_form.html')  # Kontrola použití šablony

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
        uploaded_photo_content = cls.create_test_image()
        uploaded_photo = SimpleUploadedFile(
            "image.jpg", uploaded_photo_content, content_type='image/jpeg'
        )
        cls.revision_record = RevisionRecord.objects.create(
            revision_data=cls.revision_data,
            serial_number='SN12345',
            date_manufacture=date.today(),
            date_of_first_use=date.today(),
            owner=cls.user,
            verdict='fit',
            created_by=cls.user,
            photo_of_item=uploaded_photo
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


    def test_create_revision_record_view_get(self):
        self.get_and_assert_template('add_revision_record', 'revision_form.html')

    def test_create_revision_record_view_post_valid(self):
        url = reverse('add_revision_record')
        uploaded_photo_content = self.create_test_image()
        uploaded_photo = SimpleUploadedFile(
            "image1.jpg", uploaded_photo_content, content_type='image/jpeg'
        )
        data = {
            'revision_data': self.revision_data.id,
            'serial_number': 'SN12346',
            'date_manufacture': date.today(),
            'date_of_first_use': date.today(),
            'owner': self.user.id,
            'verdict': 'fit',
            'photo_of_item': uploaded_photo
        }

        response = self.client.post(url, data, format='multipart')

        # Kontrola stavu odpovědi
        self.assertEqual(response.status_code, 302)  # 302 pro úspěšné přesměrování po vytvoření

        # Sleduj přesměrování a ověř úspěšnou zprávu
        response = self.client.post(url, data, follow=True)
        self.assertContains(response, "The item was successfully saved from CreateMixin")

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
        # Create a temporary image file to simulate file upload
        image_content = self.create_test_image()  # You will need to have this helper method to generate test image binary data
        uploaded_image = SimpleUploadedFile(
            "image.jpg", image_content, content_type="image/jpeg"
        )

        data = {
            'revision_data': self.revision_data.id,
            'serial_number': 'SNupdated',
            'date_manufacture': date.today(),
            'date_of_first_use': date.today(),
            'owner': self.user.id,
            'verdict': 'fit',
            'photo_of_item': uploaded_image  # Use uploaded image here
        }

        self.post_and_assert_redirect('edit_revision_record', data, args=[self.revision_record.id])

        # Refresh from db and check your assertions
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




