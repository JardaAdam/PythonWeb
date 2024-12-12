from datetime import timedelta
from django.utils import timezone

from django.db.models import Model, ForeignKey, CharField, DecimalField, PROTECT, FileField, ImageField, CASCADE, \
    TextField, IntegerField, DateField, ManyToManyField, OneToOneField, SET_NULL, DateTimeField

from accounts.models import CustomUser, ItemGroup
#TODO related_name kde bude potreba pro funkce
#TODO related_query_name kde bude potreba

# Create your models here.
class MaterialType(Model):
    name = CharField(max_length=32, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Material Type"
        verbose_name_plural = "Material Types"

class StandardPpe(Model):
    code = CharField(max_length=32, unique=True, blank=False, null=False)  # Kód normy (např. EN 362)
    description = TextField(blank=False, null=False)  # Popis normy

    def __str__(self):
        return self.code

class Manufacturer(Model):
    name = CharField(max_length=32, blank=False, null=False)
    material_type = ForeignKey(MaterialType, on_delete=PROTECT)
    lifetime_use_months = IntegerField(blank=False, null=False, help_text="Maximální doba používání v měsících")
    lifetime_manufacture_years = IntegerField(blank=False, null=False, help_text="Maximální doba od data výroby v letech")

    class Meta:
        verbose_name_plural = "Manufacturers"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.material_type.name}"


class TypeOfPpe(Model):
    image = ImageField(upload_to="images/", default=None)
    group_type_ppe = CharField(max_length=32, unique=True, blank=False, null=False)
    price = DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)

    def __str__(self):
        return f"{self.group_type_ppe} cena: {self.price} kč"

class RevisionData(Model):
    image = ImageField(upload_to="images/", default=None)
    manufacturer = ForeignKey(Manufacturer, on_delete=CASCADE, related_name='revisions')
    group_type_ppe = ForeignKey(TypeOfPpe, on_delete=CASCADE)
    name_ppe = CharField(max_length=32, null=False, blank=False)
    standard_ppe = ManyToManyField(StandardPpe)  # Množství norem
    # TODO dodatecne definice kolonek?
    manual_for_revision = FileField(upload_to='manuals/')

    # TODO vytvořit složku pro manuáli k revizím, images

    def __str__(self):
        return f"{self.name_ppe} ({self.group_type_ppe}) by {self.manufacturer}"

    class Meta:
        verbose_name = "Revision Data"
        verbose_name_plural = "Revision Data"

class RevisionRecord(Model):
    revision_data = ForeignKey(RevisionData, on_delete=SET_NULL)
    serial_number = CharField(max_length=64,null=False, blank=False, unique=True)
    date_manufacture = DateField(null=False, blank=False)
    date_of_first_use = DateField(null=False, blank=False)
    date_of_revision = DateField(blank=True, null=True) # automaticky vyplnovane po ukonceni vkladani!
    date_of_next_revision = DateField(null=True, blank=True) # automaticky vyplnovane po ukonceni vkladani!
    item_group = OneToOneField(ItemGroup, null=True, blank=True, on_delete=SET_NULL,
                                      related_name='revision_record')
    owner = ForeignKey(CustomUser, on_delete=SET_NULL)
    verdict = CharField(max_length=64, choices=[('new', 'New'), ('fit', 'Fit to Use'), ('retire', 'Retire')], blank=True)
    notes = TextField(blank=True)
    # TODO jake to sebou nese narocnosti na pamet?
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        # Automatické nastavení dat a výpočet nadcházející revize.
        if not self.date_of_revision:
            self.date_of_revision = timezone.now().date()
        if not self.date_of_next_revision:
            self.date_of_next_revision = self.date_of_revision + timedelta(days=365)
        super().save(*args, **kwargs)
    # TODO spravny format vypisu polozky pro vypis v hromadnem listu a pri hledani ( chci znam aspon jmeno vyrobku )
    def __str__(self):
        return f"{self.serial_number}: {self.verdict}"


