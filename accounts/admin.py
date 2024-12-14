from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Country, Company, CustomUser, ItemGroup


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'company', 'country')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('company', 'country', 'address', 'city', 'postcode',
                           'phone_number', 'business_id', 'tax_id')}),
    )
admin.site.register(Country)
admin.site.register(Company)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ItemGroup)