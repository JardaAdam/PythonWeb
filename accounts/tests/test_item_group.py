from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from accounts.models import Company, Country, ItemGroup

User = get_user_model()

class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Vytvoření společnosti
        cls.company = Company.objects.create(
            name='Test Company',
            address='Test Address',
            city='Test City',
            postcode='12345',
            phone_number='123456789',
            business_id='12345678',
            tax_id='123456789'
        )

        # Vytvoření země
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

        # Vytvoření skupin uživatelů
        cls.groups = {
            'supervisor': Group.objects.get_or_create(name='CompanySupervisor')[0],
            'company_user': Group.objects.get_or_create(name='CompanyUser')[0],
            'revision_technician': Group.objects.get_or_create(name='RevisionTechnician')[0],
        }

        # Vytvoření uživatelů
        cls.user = cls.create_user('testuser', 'testpassword', cls.groups['supervisor'])
        cls.other_user = cls.create_user('otheruser', 'password')
        cls.second_user = cls.create_user('companyuser', 'securepassword', cls.groups['company_user'])
        cls.revision_user = cls.create_user('revisiontech', 'revpassword', cls.groups['revision_technician'])
        cls.superuser = cls.create_superuser('superadmin', 'superpassword')

        # Vytvoření skupin items
        cls.item_group_user_own = ItemGroup.objects.create(name='UserOwnGroup', user=cls.second_user, company=cls.company)
        cls.item_group_user_other = ItemGroup.objects.create(name='OtherUserGroup', user=None, company=cls.company)
        cls.item_group_company = ItemGroup.objects.create(name='CompanyGroup', user=None, company=cls.company)

    @classmethod
    def create_user(cls, username, password, group=None):
        user = User.objects.create_user(username=username, password=password, first_name='First', last_name='Last')
        user.company = cls.company
        if group:
            user.groups.add(group)
        user.save()
        return user

    @classmethod
    def create_superuser(cls, username, password):
        user = User.objects.create_superuser(username=username, password=password, first_name='Super', last_name='User')
        user.company = cls.company
        user.save()
        return user

class ItemGroupDeleteViewTests(BaseTestCase):

    def test_company_user_cannot_delete_other_user_item_group(self):
        self.client.login(username='companyuser', password='securepassword')
        url = reverse('delete_item_group', args=[self.item_group_user_other.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_company_supervisor_cannot_delete_item_group_outside_company(self):
        self.client.login(username='testuser', password='testpassword')
        # Assuming this tests trying to delete an item group from a different company
        item_group_outside_company = ItemGroup.objects.create(name='OutsideCompanyGroup', company=None)
        url = reverse('delete_item_group', args=[item_group_outside_company.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_company_user_can_delete_own_item_group(self):
        self.client.login(username='companyuser', password='securepassword')
        url = reverse('delete_item_group', args=[self.item_group_user_own.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('item_group_user_list'))

    def test_company_supervisor_can_delete_companies_item_group(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('delete_item_group', args=[self.item_group_company.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('item_group_user_list'))