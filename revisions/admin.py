from django.contrib import admin

from revisions.models import Manufacturer, Expiration, Revision, TypeOfPpe

# Register your models here.
admin.site.register(Manufacturer)
admin.site.register(Expiration)
admin.site.register(TypeOfPpe)
admin.site.register(Revision)
