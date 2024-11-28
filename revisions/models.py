from datetime import date
from django.db import models
from django.db.models import Model, ManyToManyField, ForeignKey
from django.forms import CharField


# Create your models here.
class TypeOfPpe(Model):
    group_type_ppe = CharField(max_length=100)
    price =




class SheetOfPpe(Model):
    user = ForeignKey(User)
    name_ppe = ManyToManyField()
    category =
    manufacturer =
    serial_number =
    date_of_manufacture =
    date_of_first_use =
    date_of_revision =
    date_of_next_revision =
    verdict=
    notes=


class Revision(Model):
    name_ppe =
    manual_for_revision =
    lifetime_use =
    lifetime_manufacture =




