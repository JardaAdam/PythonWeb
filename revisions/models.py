from datetime import timedelta

from django.core.exceptions import ValidationError
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
    image = ImageField(upload_to='images/', blank=True, null=True)
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

class Manufacturer(Model):
    """uchovava informace ohledne zivotnosti jednotlivich polozek definovanych virobcem"""
    name = CharField(max_length=32, blank=False, null=False)
    material_type = ForeignKey(MaterialType, on_delete=PROTECT, related_name='manufacturers')
    lifetime_use_years = IntegerField(blank=False, null=False, help_text="Maximální doba používání od 1.použití v letech")
    lifetime_manufacture_years = IntegerField(blank=False, null=False, help_text="Maximální doba používání od data výroby v letech")

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
    image = ImageField(upload_to="images/",blank=False, null=False, default=None)
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

class RevisionData(Model):
    """tabulka obsahujici jednotlive polozky v prubehu plneni databaze zjednodusuje vypracovavani reviznich zaznamu"""
    image = ImageField(upload_to="images/", default=None)
    manufacturer = ForeignKey(Manufacturer, on_delete=PROTECT, related_name='revisions', related_query_name='revision')
    group_type_ppe = ForeignKey(TypeOfPpe, on_delete=PROTECT)
    name_ppe = CharField(max_length=32, null=False, blank=False)
    standard_ppe = ManyToManyField(StandardPpe, related_name='revision_data')  # Množství norem
    manual_for_revision = FileField(upload_to='manuals/')
    notes = TextField(blank=False, null=False)


    # FIXME upravit zobrazovani nazvu kolonek
    class Meta:
        verbose_name = "Revision Data"
        verbose_name_plural = "Revision Data"
        constraints = [
            UniqueConstraint(fields=['manufacturer', 'name_ppe'], name='unique_manufacturer_name_ppe')
        ]

    def __str__(self):
        return f"{self.name_ppe} ({self.group_type_ppe}) by {self.manufacturer.name}"

    def __repr__(self):
        return (f"RevisionData(id={self.id}, name_ppe='{self.name_ppe}', "
                f"manufacturer='{self.manufacturer.name}')")




class RevisionRecord(Model):
    """ uchovava informace o revizi jednotlivich polozek a ma informace potrebne k upozornovani na
        - konec platnosti revize
        - konec zivotnosti
        - upozorneni od vyrobce podle serial_number"""
    revision_data = ForeignKey(RevisionData, on_delete=PROTECT)
    serial_number = CharField(max_length=64,null=False, blank=False, unique=True)
    date_manufacture = DateField(null=False, blank=False)
    # FIXME dořešit zapisování těchto hodnot ve formuláři!!
    date_of_first_use = DateField(null=False, blank=False)
    date_of_revision = DateField(blank=True, null=True) # automaticky vyplnovane po ukonceni vkladani!
    date_of_next_revision = DateField(null=True, blank=True) # automaticky vyplnovane po ukonceni vkladani!
    item_group = ForeignKey(ItemGroup, null=True, blank=True, on_delete=PROTECT, related_name='revision_records', related_query_name='revision_record')
    owner = ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True)
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
    created_by = ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, related_name='created_revision_records')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)


    def __str__(self):
        manufacturer_name = self.revision_data.manufacturer.name if self.revision_data.manufacturer else "Neznámý výrobce"
        group_type = self.revision_data.group_type_ppe.group_type_ppe if self.revision_data.group_type_ppe else "Neznámý typ"
        name_ppe = self.revision_data.name_ppe if self.revision_data.name_ppe else "Neznámé PPE"

        return (f"{manufacturer_name} | {group_type} | {name_ppe} | "
                f"{self.serial_number} | {self.date_manufacture} | {self.date_of_first_use} | "
                f"{self.date_of_revision} | {self.date_of_next_revision} | {self.verdict} | {self.notes}")

    def __repr__(self):
        return (f"RevisionRecord(id={self.id}, serial_number='{self.serial_number}', "
                f"owner='{self.owner.username if self.owner else None}','created_by={self.created_by.username if self.created_by else None}', "
                f"verdict='{self.verdict}')")

    def clean(self):
        if not self.revision_data:
            raise ValidationError("Data revize nemohou být prázdná.")

        # Nastavení date_of_first_use na date_manufacture, pokud není zadán
        if self.date_of_first_use is None:
            self.date_of_first_use = self.date_manufacture

        # Zkontrolujeme, zda date_of_first_use >= date_manufacture
        if self.date_of_first_use < self.date_manufacture:
            raise ValidationError("Datum prvního použití nemůže být dříve než datum výroby.")

        # Získání hodnot životnosti od výrobce
        manufacturer = self.revision_data.manufacturer
        lifetime_use_years = manufacturer.lifetime_use_years
        lifetime_manufacture_years = manufacturer.lifetime_manufacture_years

        current_date = timezone.now().date()

        # Kontrola konce životnosti od prvního použití
        max_use_date = self.date_of_first_use + timedelta(days=365 * lifetime_use_years)
        if current_date > max_use_date:
            self.verdict = self.VERDICT_RETIRE
            raise ValidationError("The item has exceeded its lifetime from the first use according to manufacturer guidelines.")

        # Kontrola konce životnosti od výroby
        max_manufacture_date = self.date_manufacture + timedelta(days=365 * lifetime_manufacture_years)
        if current_date > max_manufacture_date:
            self.verdict = self.VERDICT_RETIRE
            raise ValidationError("The item has exceeded its lifetime from manufacture according to manufacturer guidelines.")

        # Zbývající dny do konce životnosti z obou pohledů
        days_until_use_expiry = (max_use_date - current_date).days
        days_until_manufacture_expiry = (max_manufacture_date - current_date).days

        # Nejkratší čas (nejsilnější omezující faktor životnosti)
        days_until_expiry = min(days_until_use_expiry, days_until_manufacture_expiry)

        # Aktualizace verdiktu a kontrola blížícího se konce životnosti
        if days_until_expiry <= 365 and self.verdict != self.VERDICT_RETIRE:
            self.verdict = self.VERDICT_FIT_UNTIL
            raise ValidationError(f"Životnost tohoto prostředku končí za {days_until_expiry} dní.")
        elif self.verdict != self.VERDICT_RETIRE:
            self.verdict = self.VERDICT_FIT

    def save(self, *args, **kwargs):
        self.full_clean()  # Spustí metodu clean()
        if not self.date_of_revision:
            self.date_of_revision = timezone.now().date()
        if not self.date_of_next_revision:
            self.date_of_next_revision = self.date_of_revision + timedelta(days=365)
        super().save(*args, **kwargs)

    # def clean(self):
    #     if not self.revision_data:
    #         raise ValidationError("Revision data cannot be None")
    #
    #     # Zkontrolujeme, zda date_of_first_use >= date_manufacture
    #     if self.date_of_first_use < self.date_manufacture:
    #         raise ValidationError("Date of first use cannot be before date of manufacture.")
    #
    #     # Získání hodnot životnosti od výrobce
    #     manufacturer = self.revision_data.manufacturer
    #     lifetime_use_years = manufacturer.lifetime_use_years
    #     lifetime_manufacture_years = manufacturer.lifetime_manufacture_years
    #
    #     # Kontrola, zda date_of_first_use nepřekračuje lifetime_use_years od prvního použití
    #     if (self.date_of_first_use + timedelta(days=365 * lifetime_use_years)) < timezone.now().date():
    #         raise ValidationError(
    #             "The item has exceeded its lifetime from the first use according to manufacturer guidelines.")
    #
    #     # Kontrola, zda date_manufacture nepřekračuje lifetime_manufacture_years od výroby
    #     if (self.date_manufacture + timedelta(days=365 * lifetime_manufacture_years)) < timezone.now().date():
    #         raise ValidationError(
    #             "The item has exceeded its lifetime from manufacture according to manufacturer guidelines.")
    #
    # def save(self, *args, **kwargs):
    #     # Ujistěte se, že se volá clean před uložením
    #     self.full_clean()  # Tímto se provede validace z clean()
    #
    #     # Automatické nastavení dat a výpočet dat nadcházející revize
    #     if not self.date_of_revision:
    #         self.date_of_revision = timezone.now().date()
    #     if not self.date_of_next_revision:
    #         self.date_of_next_revision = self.date_of_revision + timedelta(days=365)
    #
    #     super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if not self.revision_data:
    #         raise ValueError("Revision data cannot be None")
    #
    #     # Automatické nastavení dat a výpočet nadcházející revize.
    #     if not self.date_of_revision:
    #         self.date_of_revision = timezone.now().date()
    #     if not self.date_of_next_revision:
    #         self.date_of_next_revision = self.date_of_revision + timedelta(days=365)
    #     super().save(*args, **kwargs)