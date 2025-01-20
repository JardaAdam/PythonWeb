from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from .models import Country, Company, CustomUser, ItemGroup


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'company', 'country')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('company', 'country', 'address', 'city', 'postcode',
                           'phone_number', 'business_id', 'tax_id')}),
    )
# Definujeme InlineAdmin pro CustomUser
class CustomUserInline(admin.StackedInline):  # Můžete použít také '' pro vertikální zobrazení
    model = CustomUser
    extra = 1  # Pokud nechcete mít místa pro přidání nových uživatelů zde
    fields = ['username','groups']

# Definujeme CompanyAdmin class
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'city', 'phone_number']  # Pole, které chcete zobrazit v seznamu
    inlines = [CustomUserInline]  # Přidání našeho inline modelu


admin.site.register(LogEntry)
admin.site.register(ContentType)
admin.site.register(Session)
admin.site.register(Country)
admin.site.register(Company, CompanyAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ItemGroup)






