import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase
from revisions.models import *
from accounts.models import CustomUser
import datetime


class RevisionsModelsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Vytvoření základních údajů pro testování modelů
        """ User """
        cls.user = CustomUser.objects.create(username='testuser', password='testpass')
        """ Material type """
        cls.material_image = SimpleUploadedFile(
            "material_image.jpg",
            content=b"material_image_content",
            content_type="image/jpeg"
        )
        cls.material_type = MaterialType.objects.create(
            name='Helmet',
            symbol=cls.material_image
        )

        """ Standart PPE """

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

        """ Manufacturer """

        cls.manufacturer_logo = SimpleUploadedFile(
            "manufacturer_logo.jpg",
            content=b"manufacturer_logo_content",
            content_type="image/jpeg"
        )
        cls.manufacturer = Manufacturer.objects.create(
            name='Singing Rock',
            logo=cls.manufacturer_logo
        )

        """ Lifetime of PPE"""

        cls.lifetime_of_ppe = LifetimeOfPpe.objects.create(
            manufacturer=cls.manufacturer,
            material_type=cls.material_type,
            lifetime_use_years=10,
            lifetime_manufacture_years=15
        )

        """ Type of PPE """
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

        """ Revision data"""

        cls.revision_data_image = SimpleUploadedFile(
            "revision_data_image.jpg",
            content=b"revision_data_image_content",
            content_type="image/jpeg"
        )
        cls.revision_data = RevisionData.objects.create(
            image_items=cls.revision_data_image,
            lifetime_of_ppe=cls.lifetime_of_ppe,
            type_of_ppe=cls.type_of_ppe,
            name_ppe='Flash industry',
            manual_for_revision='manual.pdf'
        )
        cls.revision_data.standard_ppe.add(cls.standard_ppe)

        """ Revision record """

        cls.revision_record_image = SimpleUploadedFile(
            "revision_record_image.jpg",
            content=b"revision_record_image_content",
            content_type="image/jpeg"
        )

        cls.revision_record = RevisionRecord.objects.create(
            revision_data=cls.revision_data,
            serial_number='SN12345',
            date_manufacture=datetime.date(2020, 1, 1),
            owner=cls.user,
            photo_of_item=cls.revision_record_image,
            verdict='fit',
            created_by=cls.user,
        )
        # Vytvoření záznamu s jiným sériovým číslem pro test duplikace
        cls.revision_record_duplicate_test = RevisionRecord.objects.create(
            revision_data=cls.revision_data,
            serial_number='SNunique',
            date_manufacture=datetime.date(2020, 1, 1),
            owner=cls.user,
            photo_of_item=cls.revision_record_image,
            created_by=cls.user,
        )

    """ Material type"""

    def test_material_type_creation(self):
        self.assertEqual(self.material_type.name, 'Helmet')

    def test_material_type_image_upload(self):
        self.assertTrue(self.material_type.symbol.name.startswith('static/image/material/material_image'))

    def test_prevent_duplicate_material_type_creation(self):
        """Test that creating a material_type with a duplicate name raises an IntegrityError."""
        with self.assertRaises(IntegrityError):
            MaterialType.objects.create(
                name="Helmet",  # Duplicate name
                symbol=self.material_image
            )

    """ Standard PPE """

    def test_standard_ppe_creation(self):
        self.assertEqual(self.standard_ppe.code, 'EN 362')
        self.assertEqual(self.standard_ppe.description, 'Norma pro spojovací prostředky')

    def test_standard_ppe_image_upload(self):
        self.assertTrue(self.standard_ppe.image.name.startswith('static/image/standard_ppe/logo/standard_image'))

    def test_prevent_duplicate_standard_ppe_creation(self):
        """Test that creating a standard_ppe with a duplicate name raises an IntegrityError."""
        with self.assertRaises(IntegrityError):
            StandardPpe.objects.create(
                code="EN 362",  # Duplicate name
                image=self.standard_image
            )

    """ Manufacturer """

    def test_manufacturer_creation(self):
        self.assertEqual(self.manufacturer.name, 'Singing Rock')

    def test_manufacturer_logo_upload(self):
        self.assertTrue(self.manufacturer.logo.name.startswith('static/image/manufacturer/logo/manufacturer_logo'))

    def test_prevent_duplicate_manufacturer_creation(self):
        """Test that creating a Manufacturer with a duplicate name raises an IntegrityError."""
        with self.assertRaises(IntegrityError):
            Manufacturer.objects.create(
                name="Singing Rock",  # Duplicate name
                logo=self.manufacturer_logo
            )

    """ Lifetime of PPE """

    def test_lifetime_of_ppe_creation(self):
        """Test that LifetimeOfPpe is appropriately created."""
        self.assertEqual(self.lifetime_of_ppe.manufacturer.name, 'Singing Rock')
        self.assertEqual(self.lifetime_of_ppe.material_type.name, 'Helmet')
        self.assertEqual(self.lifetime_of_ppe.lifetime_use_years, 10)
        self.assertEqual(self.lifetime_of_ppe.lifetime_manufacture_years, 15)

    def test_cannot_create_lifetime_of_ppe_without_required_fields(self):
        """Test that creating a LifetimeOfPpe without required fields raises an error."""
        with self.assertRaises(ValidationError):
            lifetime_of_ppe_invalid = LifetimeOfPpe(
                manufacturer=self.manufacturer,
                material_type=self.material_type
            )
            lifetime_of_ppe_invalid.full_clean()

    def test_prevent_duplicate_lifetime_of_ppe_creation(self):
        """Test that creating a LifetimeOfPpe with a duplicate manufacturer and material_type raises an IntegrityError."""
        with self.assertRaises(IntegrityError):
            LifetimeOfPpe.objects.create(
                manufacturer=Manufacturer.objects.get(name="Singing Rock"),
                material_type=MaterialType.objects.get(name="Helmet"),
                lifetime_use_years=10,
                lifetime_manufacture_years=15
            )
    """ Type of PPE """

    def test_type_of_ppe_image_upload(self):
        self.assertTrue(self.type_of_ppe.image.name.startswith('static/image/type_of_ppe/type_of_ppe_image'))

    def test_type_of_ppe_creation(self):
        self.assertEqual(self.type_of_ppe.group_type_ppe, 'Helma')
        self.assertEqual(self.type_of_ppe.price, 100.00)

    def test_prevent_duplicate_type_of_ppe_creation(self):
        """Test that creating a TypeOfPpe with a duplicate group_type_ppe raises an IntegrityError."""
        with self.assertRaises(IntegrityError):
            TypeOfPpe.objects.create(
                group_type_ppe='Helma',  # Duplicate group_type_ppe
                price=100.00
            )

    """ Revision Data """

    def test_revision_data_creation(self):
        self.assertEqual(self.revision_data.name_ppe, 'Flash industry')
        self.assertTrue(self.revision_data.standard_ppe.filter(pk=self.standard_ppe.pk).exists())

    def test_revision_data_image_upload(self):
        self.assertTrue(
            self.revision_data.image_items.name.startswith('static/image/revision_data/revision_data_image'))

    def test_prevent_duplicate_revision_data_creation(self):
        """Test that creating duplicate RevisionData raises an IntegrityError."""
        with self.assertRaises(IntegrityError):
            RevisionData.objects.create(
                lifetime_of_ppe=self.revision_data.lifetime_of_ppe,
                type_of_ppe=self.revision_data.type_of_ppe,
                name_ppe='Flash industry',  # Duplicate name_ppe
                manual_for_revision=self.revision_data.manual_for_revision
            )

    """ Revision Record """

    def test_revision_record_creation(self):
        """Ensure that all required fields in RevisionRecord are correctly set and stored upon creation."""

        # Check serial number
        self.assertEqual(self.revision_record.serial_number, 'SN12345')

        # Check verdict
        self.assertEqual(self.revision_record.verdict, 'fit')

        # Check date of manufacture
        self.assertEqual(self.revision_record.date_manufacture, datetime.date(2020, 1, 1))

        # Check owner
        self.assertEqual(self.revision_record.owner.username, 'testuser')

        # Check created_by
        self.assertEqual(self.revision_record.created_by.username, 'testuser')

        # Check revision_data
        self.assertEqual(self.revision_record.revision_data.name_ppe, 'Flash industry')

        # Check date_of_first_use, assuming it should default to date of manufacture if not set
        self.assertEqual(self.revision_record.date_of_first_use, datetime.date(2020, 1, 1))

    def test_revision_record_image_upload(self):
        self.assertTrue(
            self.revision_record.photo_of_item.name.startswith('media/image/revision_record/revision_record_image'))

    def test_revision_record_valid_dates(self):
        """Test valid date setting rules on RevisionRecord."""
        self.revision_record.date_of_first_use = datetime.date(2019, 12, 31)  # Should be invalid
        with self.assertRaises(ValidationError):
            self.revision_record.full_clean()

    def test_revision_record_clean_method_invalid_dates(self):
        """Test custom clean method prevents invalid date_of_first_use with the correct error message."""
        self.revision_record.date_of_first_use = self.revision_record.date_manufacture - datetime.timedelta(days=1)

        expected_error_message = "The date of first use cannot be earlier than the date of manufacture"

        with self.assertRaises(ValidationError) as context:
            self.revision_record.full_clean()

        # Ensure that the error message contains the expected message
        self.assertIn(expected_error_message, str(context.exception))

    def test_revision_record_auto_dates(self):
        """Test automatic setting of date_of_revision and date_of_next_revision."""

        # Set the date_of_first_use to match the date of manufacture
        self.revision_record.date_of_first_use = self.revision_record.date_manufacture

        # Trigger model validation and potential auto-setting logic
        self.revision_record.clean()

        # Save the record to apply and test auto-setting logic
        self.revision_record.save()

        # Ensure date_of_revision is set
        self.assertIsNotNone(self.revision_record.date_of_revision)

        # Check date_of_next_revision is one year after date_of_revision
        self.assertEqual(
            self.revision_record.date_of_next_revision,
            self.revision_record.date_of_revision + datetime.timedelta(days=365)
        )

    # Příklad negativního testu pro vytvoření RevisionRecord bez potřebného data
    def test_creation_without_revision_data(self):
        """Test creating a RevisionRecord without 'revision_data' raises error with correct message."""
        invalid_revision = RevisionRecord(
            serial_number='SN54321',
            date_manufacture=datetime.date(2020, 1, 1),
            owner=self.user
        )

        expected_error_message = "The revision data cannot be empty"  # Change to whatever message your model raises

        with self.assertRaises(ValidationError) as context:
            invalid_revision.full_clean()

        # Ensure that the error message contains the expected message
        self.assertIn(expected_error_message, str(context.exception))

    """ test pro překročení životnosti dle data výroby. """

    def test_lifetime_restriction_exceeded(self):
        """Ensure validation error is raised when lifetime from manufacture is exceeded."""
        date_manufacture = timezone.now().date() - timedelta(
            days=(self.lifetime_of_ppe.lifetime_manufacture_years * 365 + 1))

        # Set date_of_first_use to be the same as manufacture date to test manufacture constraint alone
        revision_record = RevisionRecord(
            revision_data=self.revision_data,
            serial_number='SNOverLifetime',
            date_manufacture=date_manufacture,
            date_of_first_use=date_manufacture,  # Same as manufacture date
            owner=self.user,
            created_by=self.user
        )

        with self.assertRaises(ValidationError) as context:
            revision_record.full_clean()

        self.assertIn("The item has exceeded its lifetime from manufacture", str(context.exception))

    """  Expirace na základě prvního použití """

    def test_expiration_based_on_first_use(self):
        """Ensure validation error is raised when lifetime from first use is exceeded."""
        # # Determine relevant lifetimes
        # lifetime_use_years = self.lifetime_of_ppe.lifetime_use_years  # e.g., 10 years
        # lifetime_manufacture_years = self.lifetime_of_ppe.lifetime_manufacture_years  # e.g., 15 years

        # Setting up dates
        date_manufacture = timezone.now().date() - timedelta(days=(13 * 365))  # Manufactured 13 years ago
        date_of_first_use = timezone.now().date() - timedelta(days=(11 * 365))  # First used 11 years ago

        revision_record = RevisionRecord(
            revision_data=self.revision_data,
            serial_number='SNFirstUseExpiration',
            date_manufacture=date_manufacture,
            date_of_first_use=date_of_first_use,
            owner=self.user,
            created_by=self.user
        )

        with self.assertRaises(ValidationError) as context:
            revision_record.full_clean()

        self.assertIn("The item has exceeded its lifetime from the first use according to "
                      "manufacturer guidelines", str(context.exception))

    """ Test expirace mezi datem aktualni revize a datem dalsi revize dle prvniho pouziti """

    def test_first_use_expiration_between_current_and_next_revision(self):
        """Ensure that the clean method raises a ValidationError if the validity of the item as first used falls
        between the current and the next revision."""

        # Set manufacturing and use dates to trigger expiration warning
        current_date = timezone.now().date()
        date_manufacture = current_date - timedelta(days=11 * 365)  # Manufacturing 11 years ago
        date_of_first_use = current_date - timedelta(days=9 * 365 + 185)  # First used 9 years and 180 days ago

        # Create revision record
        revision_record = RevisionRecord(
            revision_data=self.revision_data,
            serial_number='SNBetweenExp',
            date_manufacture=date_manufacture,
            date_of_first_use=date_of_first_use,
            owner=self.user,
            created_by=self.user
        )

        # Expected message
        expected_message = f"The lifetime of this item will end in {180} days."

        # Validate and look for the expected outcome
        with self.assertRaises(ValidationError) as context:
            revision_record.full_clean()

        # Print the outcome message to terminal
        actual_message = str(context.exception)
        print(f"Validation Error: {actual_message}")

        self.assertIn(expected_message, str(context.exception))

    """ Test expirace mezi datem aktualni revize a datem dalsi revize dle roku vyroby """

    def test_expiration_between_current_and_next_revision(self):
        """Ensure that the clean method raises a ValidationError if the validity according to the item's
        production date falls between the current and the next revision."""

        # Set manufacturing and use dates to trigger expiration warning
        current_date = timezone.now().date()
        date_manufacture = current_date - timedelta(days=14 * 365 + 180)  # Manufacturing 14 years and 180 days ago
        date_of_first_use = current_date - timedelta(days=8 * 365)  # First used 8 years ago

        # Create revision record
        revision_record = RevisionRecord(
            revision_data=self.revision_data,
            serial_number='SNBetweenExp',
            date_manufacture=date_manufacture,
            date_of_first_use=date_of_first_use,
            owner=self.user,
            created_by=self.user
        )

        # Expected message
        expected_message = f"The lifetime of this item will end in {185} days."

        # Validate and look for the expected outcome
        with self.assertRaises(ValidationError) as context:
            revision_record.full_clean()

        # Print the outcome message to terminal
        actual_message = str(context.exception)
        print(f"Validation Error: {actual_message}")

        self.assertIn(expected_message, str(context.exception))

    """ Testuje integritní chybu, pokud existuje revizní záznam s už existujícím seriovim cislem """

    def test_data_integrity_error(self):
        """Ensure validation error is raised for duplicate serial number."""
        duplicate_revision_record = RevisionRecord(
            revision_data=self.revision_data,
            serial_number='SNunique',
            date_manufacture=datetime.date(2020, 1, 1),
            owner=self.user,
            created_by=self.user
        )
        with self.assertRaises(ValidationError) as context:
            duplicate_revision_record.full_clean()
        self.assertIn("Revision record with this Serial number already exists", str(context.exception))

    """ Provádí automatické nastavení dat aktuální a následující revize """

    def test_compute_revision_dates(self):
        """Ensure revision and next revision dates are set correctly on creation."""
        revision_record = RevisionRecord.objects.create(
            revision_data=self.revision_data,
            serial_number='SNDateTest',
            date_manufacture=datetime.date.today(),
            owner=self.user,
            created_by=self.user
        )
        # Check if 'date_of_next_revision' is set correctly
        expected_date_of_next_revision = revision_record.date_of_revision + timedelta(days=365)
        self.assertEqual(revision_record.date_of_next_revision, expected_date_of_next_revision)

    """ Ověřuje správnost data prvního použití, které nemůže být před datem výroby """

    def test_invalid_first_use_date(self):
        """Ensure validation error is raised when first use date is before manufacture date."""
        revision_record = RevisionRecord(
            revision_data=self.revision_data,
            serial_number='SNinvalidFirstUse',
            date_manufacture=datetime.date.today(),
            date_of_first_use=datetime.date.today() - timedelta(days=1),  # Invalid - Before manufacture
            owner=self.user,
            created_by=self.user
        )
        with self.assertRaises(ValidationError) as context:
            revision_record.full_clean()
        self.assertIn("The date of first use cannot be earlier than the date of manufacture",
                      str(context.exception))

    """ Delete test files """

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
