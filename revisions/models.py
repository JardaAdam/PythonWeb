from datetime import timedelta
from django.utils import timezone

from django.db.models import Model, ForeignKey, CharField, DecimalField, PROTECT, FileField, ImageField,  \
    TextField, IntegerField, DateField, ManyToManyField, SET_NULL, DateTimeField, UniqueConstraint

from accounts.models import CustomUser, ItemGroup
from config import settings

'''PPE = PersonalProtectiveEquipment'''
# Create your models here.

class MaterialType(Model):
    """rozdeluje polozky do jednotlivich skupin podle materialu"""
    name = CharField(max_length=32, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"MaterialType(id={self.id}, name='{self.name}')"

    class Meta:
        verbose_name = "Material Type"
        verbose_name_plural = "Material Types"

class StandardPpe(Model):
    """databaze norem pro OOPP"""
    image = ImageField(upload_to='images/', blank=False, null=False)
    code = CharField(max_length=32, unique=True, blank=False, null=False)  # Kód normy (např. EN 362)
    description = TextField(blank=False, null=False)  # Popis normy
    class Meta:
        verbose_name = "Standard PPE"
        verbose_name_plural = "Standards PPE"

    def __str__(self):
        return self.code

    def __repr__(self):
        return f"StandardPpe(id={self.id}, code='{self.code}', description='{self.description[:20]}...')"

class Manufacturer(Model):
    """uchovava informace ohledne zivotnosti jednotlivich polozek definovanych virobcem"""
    name = CharField(max_length=32, blank=False, null=False)
    material_type = ForeignKey(MaterialType, on_delete=PROTECT, related_name='manufacturers')
    lifetime_use_months = IntegerField(blank=False, null=False, help_text="Maximální doba používání v měsících")
    lifetime_manufacture_years = IntegerField(blank=False, null=False, help_text="Maximální doba od data výroby v letech")

    class Meta:
        verbose_name_plural = "Manufacturers"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.material_type.name}"

    def __repr__(self):
        return (f"Manufacturer(id={self.id}, name='{self.name}', "
                f"material_type='{self.material_type.name}')")


class TypeOfPpe(Model):
    """definuje cenu jednotlivich skupin polozek pro vypocet finalni ceny za revizi"""
    image = ImageField(upload_to="images/", default=None)
    group_type_ppe = CharField(max_length=32, unique=True, blank=False, null=False)
    price = DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)

    class Meta:
        verbose_name = "Type of PPE"
        verbose_name_plural = "Types of PPE"


    def __str__(self):
        return f"{self.group_type_ppe} cena: {self.price} kč"

    def __repr__(self):
        return (f"TypeOfPpe(id={self.id}, group_type_ppe='{self.group_type_ppe}', "
                f"price={self.price})")

class RevisionData(Model):
    """tabulka obsahujici jednotlive polozky v prubehu plneni databaze zjednodusuje vypracovavani reviznich zaznamu"""
    image = ImageField(upload_to="images/", default=None)
    manufacturer = ForeignKey(Manufacturer, on_delete=PROTECT, related_name='revisions', related_query_name='revision')
    group_type_ppe = ForeignKey(TypeOfPpe, on_delete=PROTECT)
    name_ppe = CharField(max_length=32, null=False, blank=False)
    standard_ppe = ManyToManyField(StandardPpe, related_name='revision_data')  # Množství norem
    manual_for_revision = FileField(upload_to='manuals/')
    notes = TextField(blank=False, null=False)


    # TODO vytvořit složku pro manuáli k revizím, images
    class Meta:
        constraints = [
            UniqueConstraint(fields=['manufacturer', 'name_ppe'], name='unique_manufacturer_name_ppe')
        ]

    def __str__(self):
        return f"{self.name_ppe} ({self.group_type_ppe}) by {self.manufacturer}"

    def __repr__(self):
        return (f"RevisionData(id={self.id}, name_ppe='{self.name_ppe}', "
                f"manufacturer='{self.manufacturer.name}')")

    class Meta:
        verbose_name = "Revision Data"
        verbose_name_plural = "Revision Data"

class RevisionRecord(Model):
    """ uchovava informace o revizi jednotlivich polozek a ma informace potrebne k upozornovani na
        - konec platnosti revize
        - konec zivotnosti
        - upozorneni od vyrobce podle serial_number"""
    revision_data = ForeignKey(RevisionData, on_delete=PROTECT)
    serial_number = CharField(max_length=64,null=False, blank=False, unique=True)
    date_manufacture = DateField(null=False, blank=False)
    date_of_first_use = DateField(null=False, blank=False)
    date_of_revision = DateField(blank=True, null=True) # automaticky vyplnovane po ukonceni vkladani!
    date_of_next_revision = DateField(null=True, blank=True) # automaticky vyplnovane po ukonceni vkladani!
    item_group = ForeignKey(ItemGroup, null=True, blank=True, on_delete=PROTECT, related_name='revision_records', related_query_name='revision_record')
    owner = ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True)
    VERDICT_NEW = 'new'
    VERDICT_FIT = 'fit'
    VERDICT_RETIRE = 'retire'

    VERDICT_CHOICES = [
        (VERDICT_NEW, 'New'),
        (VERDICT_FIT, 'Fit to Use'),
        (VERDICT_RETIRE, 'Retire'),
    ]
    verdict = CharField(max_length=64, choices=VERDICT_CHOICES, blank=True)
    notes = TextField(blank=True)
    created_by = ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, related_name='created_revision_records')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.revision_data:
            raise ValueError("Revision data cannot be None")

        # Automatické nastavení dat a výpočet nadcházející revize.
        if not self.date_of_revision:
            self.date_of_revision = timezone.now().date()
        if not self.date_of_next_revision:
            self.date_of_next_revision = self.date_of_revision + timedelta(days=365)
        super().save(*args, **kwargs)

    def __str__(self):
        manufacturer_name = self.revision_data.manufacturer.name if self.revision_data.manufacturer else "Neznámý výrobce"
        group_type = self.revision_data.group_type_ppe.group_type_ppe if self.revision_data.group_type_ppe else "Neznámý typ"
        name_ppe = self.revision_data.name_ppe if self.revision_data.name_ppe else "Neznámé PPE"

        return (f"{manufacturer_name} | {group_type} | {name_ppe} | "
                f"{self.serial_number} | {self.date_manufacture} | {self.date_of_first_use} | "
                f"{self.date_of_revision} | {self.date_of_next_revision} | {self.verdict} | {self.notes}")

    def __repr__(self):
        return (f"RevisionRecord(id={self.id}, serial_number='{self.serial_number}', "
                f"owner='{self.owner.username if self.owner else None}', "
                f"verdict='{self.verdict}')")


