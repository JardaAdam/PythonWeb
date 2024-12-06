from datetime import date
from django.db import models
from django.db.models import Model, ManyToManyField, ForeignKey, CharField, DateTimeField, TextField, DecimalField, \
    CASCADE, SET_NULL, ImageField, URLField, FileField

from accounts.models import Profile


# Create your models here.


class TypeOfPpe(Model):
    group_type_ppe = CharField(max_length=32, null=False, blank=False, unique=True)
    price = DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.group_type_ppe} cena: {self.price} kč"

class Expiration(Model):
    manufacturer = CharField(max_length=32, null=False, blank=False)
    material = CharField(max_length=32, null=False, blank=False)
    lifetime_use = CharField(max_length=32, null=False, blank=False)
    lifetime_manufacture = CharField(max_length=32, null=False, blank=False)

    def __str__(self):
        return f"{self.manufacturer} {self.material}"

    def __repr__(self):
        return f"{self.manufacturer} {self.material} {self.lifetime_use}"

class Revision(Model):
    image = ImageField(upload_to="images/", default=None, null=False, blank=False)
    group_type_ppe = ForeignKey(TypeOfPpe, null=False, blank=False, on_delete=CASCADE, related_name='revisions')
    name_ppe = CharField(max_length=32, null=False, blank=False)
    manufacturer = ForeignKey(Expiration, null=False, blank=False, on_delete=CASCADE, related_name='revisions')
    standard_ppe = CharField(max_length=32, null=False, blank=False)
    manual_for_revision = FileField(upload_to='manuals/', null=False, blank=False)
    # lifetime_use =
    # lifetime_manufacture =
# TODO vytvořit složku pro manuáli k revizím
    def __str__(self):
        return f"{self.group_type_ppe} {self.name_ppe} {self.manufacturer}"





# TODO jakým mechanizmem bude dedit tato tabulka
# class SheetOfPpe(Model):
#     profile = ForeignKey(Profile, null=False, blank=False, on_delete=CASCADE, related_name='owner_ppe')
#     sheet_name = ForeignKey(ProfileItemList, null=False, blank=False, on_delete=SET_NULL, related_name='list_ppe')
#     group_type_ppe = ForeignKey(TypeOfPpe, null=False, blank=False, on_delete=SET_NULL, related_name='')
#     name_ppe = ForeignKey("revision.Revision", null=False, blank=False, on_delete=SET_NULL, related_name='name_ppe')
#     standard_ppe = ForeignKey("revision.Revision", null=False, blank=False, on_delete=SET_NULL, related_name='standard_ppe')
#     manufacturer =
#     serial_number =
#     date_of_manufacture =
#     date_of_first_use =
#     date_of_revision =
#     date_of_next_revision =
#     verdict =
#     notes =

# class ProfileItemList(Model):
#     profile = ForeignKey(Profile, null=False, blank=False, on_delete=CASCADE, related_name='items_lists')
#     sheet_name = CharField(max_length=32, null=False, blank=False)
#     create = DateTimeField(auto_now_add=True)
#     update = DateTimeField(auto_now=True)
#     information = TextField(null=True, blank=True)
#
#     class Meta:
#         ordering = ['profile']
#         constraints = [
#             models.UniqueConstraint(fields=['profile', 'sheet_name'], name='unique_sheet_per_profile')
#         ]




