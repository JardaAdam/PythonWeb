from django.contrib import admin


# Register your models here.
from accounts.models import Profile
admin.site.register(Profile)
# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'discount']
#     # TODO přispůsobit modelu Profile