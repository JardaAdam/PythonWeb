from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from accounts.forms import CompanyForm
from accounts.models import CustomUser, Company, Country, ItemGroup
from config.test_base_view import BaseViewsTest



class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Vytvoření testovacího uživatele a společnosti
        cls.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='Testak',
            last_name='Testovic',
            address='Nova 102',
            city='Nova')
        supervisor_group, created = Group.objects.get_or_create(name='CompanySupervisor')
        cls.user.groups.add(supervisor_group)

        cls.company = Company.objects.create(
            name='Test Company',
            address='Test Address',
            city='Test City',
            postcode='12345',
            phone_number='123456789',
            business_id='12345678',
            tax_id='123456789'
        )
        cls.user.company = cls.company
        cls.user.save()

        cls.country = Country.objects.create(
            name='Czech Republic',
            postcode_validator=r"\d{5}",
            postcode_format='12345',
            phone_number_prefix="+420",
            phone_number_validator=r"^(?:\+420)?\d{9}$",
            phone_number_format='123456789',
            business_id_validator=r"^\d{8}$",
            business_id_format='12345678',
            tax_id_prefix="CZ",
            tax_id_validator=r"\d{10}$",
            tax_id_format='1234567890',
        )
        cls.item_group = ItemGroup.objects.create(
            name='Test group',
            user=cls.user,
            company=cls.company
        )
        cls.user.save()

        # Přidáme dalšího uživatele pro testy, kde to bude potřeba
        cls.other_user = CustomUser.objects.create_user(username='otheruser', password='password')
        cls.other_user.company = cls.company
        cls.other_user.save()

        # Vytvoření u prověření `CompanyUser`
        company_user_group, created = Group.objects.get_or_create(name='CompanyUser')

        # Druhý uživatel ve stejné společnosti s právy `CompanyUser`
        cls.second_user = CustomUser.objects.create_user(
            username='companyuser',
            password='securepassword',
            first_name='Obycejny',
            last_name='Uzivatel'
        )

        cls.second_user.company = cls.company
        cls.second_user.groups.add(company_user_group) # Přidání uživatele do skupiny `CompanyUser`
        cls.second_user.save()

        cls.second_item_group = ItemGroup.objects.create(
            name='Companyusergroup',
            user=cls.second_user,
            company=cls.company
        )

        # Vytvoření uživatele `RevisionTechnician`
        revision_technician_group, created = Group.objects.get_or_create(name='RevisionTechnician')
        cls.revision_user = CustomUser.objects.create_user(
            username='revisiontech',
            password='revpassword',
            first_name='Revizni',
            last_name='Technik'
        )
        cls.revision_user.company = cls.company
        cls.revision_user.groups.add(revision_technician_group)
        cls.revision_user.save()

        # Vytvoření uživatele `SuperUser`
        cls.superuser = CustomUser.objects.create_superuser(
            username='superadmin',
            password='superpassword',
            first_name='Super',
            last_name='Admin'
        )
        cls.superuser.company = cls.company
        cls.superuser.save()


class CustomUserViewTest(BaseTestCase):
    def test_custom_user_view_loads_correctly(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)


class CustomUserUpdateViewTest(BaseTestCase):
    def test_update_user_profile_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit_profile'), {
            'first_name': 'Updatedname',
            'last_name': 'Updatedlastname',
            'email': self.user.email,
            'address': 'Pondelni 100'
        })
        # Zkontrolujeme přítomnost chyb a jejich výpis
        if 'form' in response.context:
            print(response.context['form'].errors)

        # Zkontrolujeme, zda došlo k přesměrování
        self.assertRedirects(response, reverse('profile'))

        # Refresh instance uživatele a zkontrolujte změny
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updatedname')

    def test_update_user_profile_failure(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit_profile'), {
            'first_name': '',  # neplatná data
            'last_name': '',
            'email': self.user.email,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')  # Zkontroluj přesné znění chybové zprávy


class CompanyListViewTest(BaseTestCase):
    def test_company_list_display(self):
        self.client.login(username='revisiontech', password='revpassword')
        response = self.client.get(reverse('company_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.company.name)


class CompanyViewTest(BaseTestCase):
    def test_access_company_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('company_detail', args=[self.company.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.company.name)

class CompanyCreateViewTest(BaseTestCase):
    def test_company_create_view_loads_correctly(self):
        self.client.login(username='testuser', password='testpassword')
        supervisor_group, created = Group.objects.get_or_create(name='CompanySupervisor')
        response = self.client.get(reverse('add_company'))
        self.assertEqual(response.status_code, 200)
        # Ověří, že používáme správnou šablonu
        self.assertTemplateUsed(response, 'account_form.html')

    def test_company_create_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_company'), {
            'name': 'New TestCompany',
            'country': self.country.pk,
            'address': '123 Test Address',
            'city': 'Test City',
            'postcode': '12345',
            'phone_number': '123456789',
            'company_email': 'test@email.com',
            'business_id': '12345678',
            'tax_id': '8765432101'
        })
        self.assertEqual(response.status_code, 302)  # Předpokládáme, že po úspěšném vytváření dojde k přesměrování
        self.assertTrue(Company.objects.filter(name='New TestCompany').exists())

    def test_company_create_success_message(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_company'), {
            'name': 'New TestCompany',
            'country': self.country.pk,
            'address': '123 Test Address',
            'city': 'Test City',
            'postcode': '12345',
            'phone_number': '123456789',
            'company_email': 'test@email.com',
            'business_id': '12345678',
            'tax_id': '8765432121'
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Company added successfully and you have been assigned to it.")

    def test_company_create_invalid_data(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_company'), {
            'name': '',
            'country': self.country.pk,
            'address': '',
            'city': '',
            'postcode': '150 23',
            'phone_number': '123654',
            'business_id': '2156',
            'tax_id': '54948'
        })
        # Ujisti se, že se vrátí na formulářovou stránku
        self.assertEqual(response.status_code, 200)

        # Kontrola, zda form je v kontextu a obsahuje chyby
        self.assertIn('form', response.context)
        form = response.context['form']

        # Potvrď chyby form
        self.assertTrue(form.errors)

        # Ruční kontrola chyb pro každé pole
        self.assertIn('name', form.errors)
        self.assertIn('This field is required.', form.errors['name'])

        # self.assertIn('country', form.errors)
        # self.assertIn('This field is required.', form.errors['country'])

        self.assertIn('address', form.errors)
        self.assertIn('This field is required.', form.errors['address'])

        self.assertIn('city', form.errors)
        self.assertIn('This field is required.', form.errors['city'])

        self.assertIn('postcode', form.errors)
        self.assertIn('The postcode does not match the format for the selected country Czech Republic. Expected format is: 12345.', form.errors['postcode'])

        self.assertIn('phone_number', form.errors)
        self.assertIn('The phone number does not match the format for the selected country Czech Republic. Expected format is: 123456789.', form.errors['phone_number'])

        self.assertIn('business_id', form.errors)
        self.assertIn('The Business ID does not match the format for the selected country Czech Republic. Expected format is: 12345678.', form.errors['business_id'])

        self.assertIn('tax_id', form.errors)
        self.assertIn('The Tax ID does not match the format for the selected country Czech Republic. Expected format is: 1234567890.', form.errors['tax_id'])


class CompanyUpdateViewTest(BaseTestCase):
    def test_successful_company_update(self):
        """ company record editing by a user belonging to this company """
        self.client.login(username='testuser', password='testpassword')
        self.company = Company.objects.get(pk=self.company.pk)
        # Nastavení URL pro úpravu společnosti s parametrem "next"
        edit_url = reverse('edit_company', args=[self.user.company.pk])
        previous_url  = reverse('company_view')
        url_with_next = f"{edit_url}?next={previous_url}"

        response = self.client.post(url_with_next, {
            'name': 'UpdatedCompanyName',
            'country': self.company.pk,
            'address': "Podebradova 712",
            'city': 'Praha',
            'postcode': '25082',
            'phone_number': '666555888',
            'company_email': 'test@email.com',
            'business_id': '12345678',
            'tax_id': '1234567898'
        })
        if response.status_code == 200:
            print(response.context['form'].errors)  # Přidej tento řádek pro výpis chyb

        self.assertRedirects(response, previous_url)
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, 'UpdatedCompanyName')


class ItemGroupTestCase(BaseTestCase):
    def test_item_group_creation(self):
        self.assertEqual(self.item_group.name, 'Test group')
        self.assertEqual(self.item_group.user, self.user)
        self.assertEqual(self.item_group.company, self.company)

    def test_unique_constraint(self):
        # Zkusit vytvořit skupinu se stejným jménem od stejného uživatele a firmy
        with self.assertRaises(Exception):
            ItemGroup.objects.create(
                name='Test group',
                user='testuser',
                company=self.company
            )

    def test_item_group_str(self):
        self.assertEqual(str(self.item_group),'Item group: Test group | User: Testak Testovic | Company: Test Company')

    # Testy pro CRUD operace nad pohledy
    def test_item_group_list_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('item_group_company_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test group')

    def test_item_group_detail_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('item_group_detail', args=[self.item_group.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test group')

    def test_item_group_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_item_group'), {
            'name': 'Another Group',
            'user': self.user.pk,
            'company': self.company.pk
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ItemGroup.objects.filter(name='Another group').exists())

    def test_item_group_create_by_companyuser_view(self):
        self.client.login(username='companyuser', password='securepassword')
        response = self.client.post(reverse('add_item_group'), {
            'name': 'Another Group',
            'user': self.user.pk,
            'company': self.company.pk
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ItemGroup.objects.filter(name='Another group').exists())

    def test_duplicate_item_group_creation_by_company_user(self):
        self.client.login(username='companyuser', password='securepassword')
        user_id = CustomUser.objects.get(username='companyuser').id
        # Pokus o vytvoření duplicity
        response = self.client.post(reverse('add_item_group'), {
            'name': 'Companyusergroup',
            'user': user_id,
            'company': self.company.pk
        })

        # Kontrola, že se duplikát nevytvořil a zobrazuje se chybová hláška
        self.assertEqual(response.status_code, 200)  # Očekáváme, že zůstane na stránce formuláře.
        form = response.context['form']
        # Ověření, že v chybách formuláře je daná chybová zpráva
        self.assertIn('This item group name is already used for this user and company.', form.non_field_errors())

    def test_duplicate_item_group_creation_by_company_supervisor(self):
        self.client.login(username='testuser', password='testpassword')
        # Získejte ID uživatele
        user_id = CustomUser.objects.get(username='testuser').id
        # Simulujte vytvoření duplicity
        response = self.client.post(reverse('add_item_group'), {
            'name': 'Test group',
            'user': user_id,
            'company': self.company.pk
        })
        # Zajistěte, že kód odpovědi je 200 (formulář neprošel a zůstal na stránce)
        self.assertEqual(response.status_code, 200)
        # Extrakce formuláře z kontextu
        form = response.context['form']
        # Ověření, že v chybách formuláře je daná chybová zpráva
        self.assertIn('This item group name is already used for this user and company.', form.non_field_errors())


    def test_item_group_update_view(self):
        self.client.login(username='testuser', password='testpassword')

        # Provede POST request pro aktualizaci ItemGroup
        response = self.client.post(reverse('edit_item_group', args=[self.item_group.pk]), {
            'name': 'Updated Group',
            'user': self.user.pk,
            'company': self.company.pk
        })

        # Ujistěte se, že přesměrování zahrnuje argument pk, potřebný pro detailní pohled
        self.assertRedirects(response, reverse('item_group_detail', kwargs={'pk': self.item_group.pk}))

        # Aktualizace objektu z databáze a kontrola, že jméno bylo správně aktualizováno
        self.item_group.refresh_from_db()
        self.assertEqual(self.item_group.name, 'Updated group')

    def test_item_group_update_by_companyuser_view(self):
        self.client.login(username='companyuser', password='securepassword')

        # Provede POST request pro aktualizaci ItemGroup
        response = self.client.post(reverse('edit_item_group', args=[self.item_group.pk]), {
            'name': 'Updated Group',
            'user': self.user.pk,
            'company': self.company.pk
        })

        # Ujistěte se, že přesměrování zahrnuje argument pk, potřebný pro detailní pohled
        self.assertRedirects(response, reverse('item_group_detail', kwargs={'pk': self.item_group.pk}))

        # Aktualizace objektu z databáze a kontrola, že jméno bylo správně aktualizováno
        self.item_group.refresh_from_db()
        self.assertEqual(self.item_group.name, 'Updated group')

    def test_duplicate_item_group_update_by_company_user(self):
        self.client.login(username='companyuser', password='securepassword')
        user_id = CustomUser.objects.get(username='companyuser').id
        # Vytvoření jiného skupinového záznamu pro sestavení scénáře testu
        duplicate_group = ItemGroup.objects.create(name='Duplicate group', user=self.second_user, company=self.company)

        # Pokus o aktualizaci na duplicitní záznam
        response = self.client.post(reverse('edit_item_group', args=[duplicate_group.pk]), {
            'name': 'Companyusergroup',
            'user': user_id,
            'company': self.company.pk
        })

        # Kontrola, že aktualizace neproběhla a zobrazuje se chybová hláška
        self.assertEqual(response.status_code, 200)  # Očekáváme, že zůstane na stránce formuláře.
        # Extrakce formuláře z kontextu a kontrola na chyby
        form = response.context['form']

        # Ověřuje, zda formulář skutečně obsahuje očekávanou chybovou zprávu
        self.assertIn('This item group name is already used for this user and company.', form.non_field_errors())



    def test_duplicate_item_group_update_by_company_supervisor(self):
        self.client.login(username='testuser', password='testpassword')
        user_id = CustomUser.objects.get(username='testuser').id
        # Vytvoření jiného skupinového záznamu pro sestavení scénáře testu
        duplicate_group = ItemGroup.objects.create(name='Duplicate Group', user=self.user, company=self.company)

        # Pokus o aktualizaci na duplicitní záznam
        response = self.client.post(reverse('edit_item_group', args=[duplicate_group.pk]), {
            'name': 'Test group',
            'user': user_id,
            'company': self.company.pk
        })

        # Kontrola, že aktualizace neproběhla a zobrazuje se chybová hláška
        self.assertEqual(response.status_code, 200)  # Očekáváme, že zůstane na stránce formuláře.
        # Extrakce formuláře z kontextu
        form = response.context['form']

        # Ověření, že v chybách formuláře je daná chybová zpráva
        self.assertIn('This item group name is already used for this user and company.', form.non_field_errors())

    def test_item_group_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete_item_group', args=[self.item_group.pk]))
        self.assertRedirects(response, reverse('item_group_user_list'))
        self.assertFalse(ItemGroup.objects.filter(pk=self.item_group.pk).exists())

class CompanyTestCase(BaseTestCase):
    def test_default_country_initialization(self):
        form = CompanyForm()

        # Zajistit, že `country` je nastaven na "Czech Republic"
        czech_republic = Country.objects.get(name='Czech Republic')

        # Ověř, že výchozí hodnota je nastavena na Czech Republic
        self.assertEqual(form.fields['country'].initial, czech_republic.id,
                         "Form's default country should be 'Czech Republic'.")




class PasswordResetTest(BaseViewsTest):


    def test_reset_password_successfully(self):
        # Nejprve otestujte úspěšné ověření
        self.client.post(reverse('forgot_password'), {
            'username': 'testuser',
            'helmet_name': 'Flash industry',
            'helmet_manufacturer': 'Test Manufacturer',
        })

        # Poté zkuste resetovat heslo
        response = self.client.post(reverse('password_reset', args=[self.user.id]), {
            'new_password': 'newpass123',
            'confirm_password': 'newpass123',
        })

        # Očekáváme přesměrování po úspěšném resetování hesla
        self.assertRedirects(response, reverse('login'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass123'))

    def test_reset_password_mismatch(self):
        response = self.client.post(reverse('password_reset', args=[self.user.id]), {
            'new_password': 'newpass123',
            'confirm_password': 'wrongpass123',
        })

        # Očekáváme, že formulář obsahuje chybu
        form = response.context['form']
        self.assertIn('confirm_password', form.errors)
        self.assertIn("Passwords do not match!", form.errors['confirm_password'])