from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Model, OneToOneField, CASCADE, CharField, DecimalField

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

""" validace napríč backend """
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Telefonní číslo musí být ve formátu: '+420123456789'. Až 15 číslic je povoleno."
)

def validate_discount(value):
    if value < 0 or value > 100:
        raise ValidationError("Sleva musí být mezi 0 a 100%.")
# TODO použití AbstractUser pro základní funkcionalitu a
#  Profile použít jen pro položky které nejsou v User
# Create your models here.
class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    company_name = CharField(max_length=32, null=True, blank=True)
    address = CharField(max_length=128, null=True, blank=True)
    city = CharField(max_length=32, null=True, blank=True)
    state = CharField(max_length=32, null=True, blank=True)
    phone_number = CharField(
        validators=[phone_regex],
        max_length=17,  # +420123456789 = 13 znaků, ale ponechte rezervu
        blank=True,
        null=True,
        help_text="Zadejte telefonní číslo v mezinárodním formátu, např. +420123456789."
    )
    ICO = CharField(max_length=32, null=True, blank=True)
    DIC = CharField(max_length=32, null=True, blank=True)
    discount = DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[validate_discount],
        help_text="Zadejte slevu v procentech (např. 10.5 = 10.5%).")


