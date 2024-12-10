from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('company_name', 'address', 'city', 'postcode', 'phone_number', 'ico', 'dic', 'discount')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)