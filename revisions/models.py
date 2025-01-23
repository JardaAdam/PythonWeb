import os
from datetime import timedelta

from django.core.exceptions import ValidationError

from django.utils import timezone

from django.db.models import Model, ForeignKey, CharField, DecimalField, PROTECT, FileField, ImageField, \
    TextField, IntegerField, DateField, ManyToManyField, SET_NULL, DateTimeField, UniqueConstraint, BooleanField

from accounts.models import ItemGroup, Company
from django.conf import settings

'''PPE = PersonalProtectiveEquipment'''
# Create your models here.

# TODO vyřešit mazani obrazku společně se zaznamem
# TODO ukladani created by u vsech polozek na urovni databaze s udaji o tom kdy
class MaterialType(Model):
    """rozdeluje polozky do jednotlivich skupin podle materialu"""
    symbol = ImageField(upload_to='static/image/material/', null=True, blank=True)
    name = CharField(max_length=32, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"MaterialType(id={self.id}, name='{self.name}')"

    class Meta:
        verbose_name = "Material Type"
        verbose_name_plural = "Material Types"

    def delete(self, *args, **kwargs):
        # Delete associated files if they exist
        if self.symbol and os.path.isfile(self.symbol.path):
            os.remove(self.symbol.path)

        super().delete(*args, **kwargs)

class StandardPpe(Model):
    """databaze norem pro OOPP"""
    image = ImageField(upload_to='static/image/standard_ppe/logo/', blank=True, null=True)
    code = CharField(max_length=32, unique=True, blank=False, null=False)  # Kód normy (např. EN 362)
    description = TextField(blank=False, null=False)  # Popis normy
    class Meta:
        ordering = ['code']
        verbose_name = "Standard PPE"
        verbose_name_plural = "Standards PPE"

    def __str__(self):
        return self.code

    def __repr__(self):
        return f"StandardPpe(id={self.id}, code='{self.code}', description='{self.description[:20]}...')"

    def delete(self, *args, **kwargs):
        # Delete associated files if they exist
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)

        super().delete(*args, **kwargs)

class Manufacturer(Model):
    """Uchovává základní informace o výrobci."""
    logo = ImageField(upload_to='static/image/manufacturer/logo/', blank=True, null=True)  # logo vyrobce
    name = CharField(max_length=32,unique=True, blank=False, null=False)


    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Manufacturer(id={self.id}, name='{self.name}')"

    def delete(self, *args, **kwargs):
        # Delete associated files if they exist
        if self.logo and os.path.isfile(self.logo.path):
            os.remove(self.logo.path)

        super().delete(*args, **kwargs)
class LifetimeOfPpe(Model):
    """uchovava informace ohledne zivotnosti jednotlivich polozek definovanych virobcem"""
    manufacturer = ForeignKey(Manufacturer, on_delete=PROTECT, related_name='lifetimes')
    material_type = ForeignKey(MaterialType, on_delete=PROTECT, related_name='lifetimes')
    lifetime_use_years = IntegerField(blank=False, null=False,
                                      help_text="Maximum period of use from 1st use in years")
    lifetime_manufacture_years = IntegerField(blank=False, null=False,
                                              help_text="Maximum period of use from date of manufacture in years")

    class Meta:
        constraints = [
            UniqueConstraint(fields=['manufacturer', 'material_type'], name='unique_constraint_material_type')
        ]
        verbose_name_plural = "Lifetime of PPE"
        ordering = ['manufacturer', 'material_type']

    def __str__(self):
        return f"{self.manufacturer.name} - {self.material_type.name}"

    def __repr__(self):
        return (f"LifetimeOfPpe(id={self.id}, Manufacturer='{self.manufacturer.name}', "
                f"material_type='{self.material_type.name}')")


class TypeOfPpe(Model):
    """definuje cenu jednotlivich skupin polozek pro vypocet finalni ceny za revizi"""
    image = ImageField(upload_to="static/image/type_of_ppe/",blank=True, null=True, default=None)
    group_type_ppe = CharField(max_length=32, unique=True, blank=False, null=False)
    price = DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)

    class Meta:
        verbose_name = "Type of PPE"
        verbose_name_plural = "Types of PPE"


    def __str__(self):
        return f"{self.group_type_ppe} cena: {self.price:.2f} kč"

    def __repr__(self):
        return (f"TypeOfPpe(id={self.id}, group_type_ppe='{self.group_type_ppe}', "
                f"price={self.price})")

    def delete(self, *args, **kwargs):
        # Delete associated files if they exist
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)

        super().delete(*args, **kwargs)

class RevisionData(Model):
    # TODO pridat checked_data BooleanField ktery se v pripade pridani noveho zaznamu nekym jinym nez SuperUserem nastavi na False
    """Tabulka obsahující jednotlivé položky v průběhu plnění databáze - zjednodušuje zpracování revizních záznamů."""
    image_items = ImageField(upload_to="static/image/revision_data/", default=None)
    lifetime_of_ppe = ForeignKey(LifetimeOfPpe, on_delete=PROTECT, related_name='revision_datas')
    type_of_ppe = ForeignKey(TypeOfPpe, on_delete=PROTECT, blank=False, null=False, related_name='group_type')
    name_ppe = CharField(max_length=32, null=False, blank=False)
    standard_ppe = ManyToManyField(StandardPpe, related_name='standards_ppe')  # Množství norem
    manual_for_revision = FileField(upload_to='static/revision_data/manuals/')
    notes = TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Revision Data"
        verbose_name_plural = "Revision Data"
        constraints = [
            UniqueConstraint(fields=['lifetime_of_ppe', 'name_ppe'], name='unique_lifetime_name_ppe')
        ]

    def __str__(self):
        return f"{self.name_ppe} ({self.type_of_ppe}) by {self.lifetime_of_ppe.manufacturer.name}"

    def __repr__(self):
        return (f"RevisionData(id={self.id}, name_ppe='{self.name_ppe}', "
                f"manufacturer='{self.lifetime_of_ppe.manufacturer.name}')")

    def delete(self, *args, **kwargs):
        # Delete associated files if they exist
        if self.image_items and os.path.isfile(self.image_items.path):
            os.remove(self.image_items.path)
        if self.manual_for_revision and os.path.isfile(self.manual_for_revision.path):
            os.remove(self.manual_for_revision.path)

        # Call the delete function of the parent class
        super().delete(*args, **kwargs)



class RevisionRecord(Model):
    """ uchovava informace o revizi jednotlivich polozek a ma informace potrebne k upozornovani na
        - konec platnosti revize
        - konec zivotnosti
        - upozorneni od vyrobce podle serial_number"""
    photo_of_item = ImageField(upload_to='media/image/revision_record/', blank=True, null=True)
    revision_data = ForeignKey(RevisionData, on_delete=PROTECT)
    serial_number = CharField(max_length=64,null=False, blank=False, unique=True)
    date_manufacture = DateField(null=True, blank=True)
    # FIXME dořešit zapisování těchto hodnot ve formuláři!!
    date_of_first_use = DateField(null=True, blank=True)
    date_of_revision = DateField(blank=True, null=True) # automaticky vyplnovane po ukonceni vkladani!
    date_of_next_revision = DateField(null=True, blank=True) # automaticky vyplnovane po ukonceni vkladani!
    item_group = ForeignKey(ItemGroup, null=True, blank=True, on_delete=PROTECT, related_name='revision_records',
                            related_query_name='revision_record')
    owner_company = ForeignKey(Company, on_delete=SET_NULL,null=True, related_name='company_records',)
    owner = ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, related_name='owner_records')
    VERDICT_NEW = 'new'
    VERDICT_FIT = 'fit'
    VERDICT_RETIRE = 'retire'
    VERDICT_FIT_UNTIL = 'Fit Until'
    VERDICT_CHOICES = [
        (VERDICT_NEW, 'New'),
        (VERDICT_FIT, 'Fit to Use'),
        (VERDICT_RETIRE, 'Retire'),
        (VERDICT_FIT_UNTIL, 'Fit Until'),
    ]
    verdict = CharField(max_length=64, choices=VERDICT_CHOICES, blank=True)
    notes = TextField(blank=True)
    created_by = ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True,
                            related_name='created_revision_records')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    checked_record = BooleanField(default=False)  # kdyz zadava zaznam uzivatel upozorneni na provedeni controli zaznamu


    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['serial_number', 'owner', 'item_group', 'revision_data'],
                name='unique_serial_owner_group_revision_record'
            )
        ]

    def __str__(self):
        manufacturer_name = self.revision_data.lifetime_of_ppe.manufacturer.name if (
            self.revision_data.lifetime_of_ppe.manufacturer) else "Unknown manufacturer"
        group_type = self.revision_data.type_of_ppe.group_type_ppe if self.revision_data.type_of_ppe \
            else "Unknown type"
        name_ppe = self.revision_data.name_ppe if self.revision_data.name_ppe else "Unknown PPE"

        return (f"{manufacturer_name} | {group_type} | {name_ppe} | "
                f"{self.serial_number} | {self.date_manufacture} | {self.date_of_first_use} | "
                f"{self.date_of_revision} | {self.date_of_next_revision} | {self.verdict} | {self.notes}")

    def __repr__(self):
        return (f"RevisionRecord(id={self.id}, serial_number='{self.serial_number}', "
                f"owner='{self.owner.username if self.owner else None}','created_by={self.created_by.username if 
                self.created_by else None}', "
                f"verdict='{self.verdict}')")

    def clean(self):
        if not self.revision_data_id:
            raise ValidationError("The revision data cannot be empty")

        # Zkontrolujeme, zda date_of_first_use >= date_manufacture
        if self.date_of_first_use is not None and self.date_of_first_use < self.date_manufacture:
            raise ValidationError("The date of first use cannot be earlier than the date of manufacture")

        # Získání hodnot životnosti z LifetimeOfPpe
        lifetime_info = self.revision_data.lifetime_of_ppe
        lifetime_use_years = lifetime_info.lifetime_use_years
        lifetime_manufacture_years = lifetime_info.lifetime_manufacture_years

        current_date = timezone.now().date()

        # Zjistit max. použití a výrobu datum
        max_manufacture_date = self.date_manufacture + timedelta(days=365 * lifetime_manufacture_years)
        max_use_date = (self.date_of_first_use or self.date_manufacture) + timedelta(days=365 * lifetime_use_years)


        # Kontrola přesažení životnosti
        if current_date > max_manufacture_date:
            self.verdict = self.VERDICT_RETIRE
            raise ValidationError(
                "The item has exceeded its lifetime from manufacture")

        if current_date > max_use_date:
            self.verdict = self.VERDICT_RETIRE
            raise ValidationError(
                "The item has exceeded its lifetime from the first use according to manufacturer guidelines.")


        # Zbývající dny do konce životnosti
        days_until_use_expiry = (max_use_date - current_date).days
        days_until_manufacture_expiry = (max_manufacture_date - current_date).days

        # Nejkratší čas (nejsilnější omezující faktor životnosti)
        days_until_expiry = min(days_until_use_expiry, days_until_manufacture_expiry)

        # Aktualizace verdiktu a kontrola blížícího se konce životnosti
        if days_until_expiry <= 365:
            if self.verdict != self.VERDICT_RETIRE:
                # Nastavit 'Fit Until' a pole next revision nastavit jako None
                self.verdict = self.VERDICT_FIT_UNTIL
                self.date_of_revision = current_date
                self.date_of_next_revision = None
                raise ValidationError(f"The lifetime of this item will end in {days_until_expiry} days.")
        elif self.verdict != self.VERDICT_RETIRE:
            self.verdict = self.VERDICT_FIT

    def save(self, *args, **kwargs):
        # Nastavení date_of_first_use na date_manufacture, pokud není zadáno
        if not self.date_of_first_use:
            self.date_of_first_use = self.date_manufacture

        self.full_clean()  # Spustí metodu clean()

        if not self.date_of_revision:
            self.date_of_revision = timezone.now().date()

        # Automatické nastavení data následující revize pouze pokud není nastavena v clean()
        if self.date_of_next_revision is None:
            self.date_of_next_revision = self.date_of_revision + timedelta(days=365)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete associated files if they exist
        if self.photo_of_item and os.path.isfile(self.photo_of_item.path):
            os.remove(self.photo_of_item.path)

        super().delete(*args, **kwargs)

