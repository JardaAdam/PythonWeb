from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def assign_company_supervisor_group(sender, instance, created, **kwargs):
   if created:  # Pouze při vytváření nového uživatele
       ''' když se registruje novy uzivatel automaticky se mu nastavi PermissionGroup'''
       if instance.company:  # Pokud uživatel vybere stávající company
           # Získání nebo vytvoření skupiny CompanyUser
           company_user_group, _ = Group.objects.get_or_create(name='CompanyUser')
           instance.groups.add(company_user_group)
       else:
           # Získání nebo vytvoření skupiny CompanySupervisor
           company_supervisor_group, created = Group.objects.get_or_create(name='CompanySupervisor')
           instance.groups.add(company_supervisor_group)