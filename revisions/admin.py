from django.contrib import admin

from revisions.models import Expiration, Revision, TypeOfPpe

# Register your models here.
admin.site.register(Expiration)
admin.site.register(Revision)
admin.site.register(TypeOfPpe)