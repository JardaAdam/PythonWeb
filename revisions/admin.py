from django.contrib import admin

from revisions.models import MaterialType,StandardPpe, Manufacturer,LifetimeOfPpe, TypeOfPpe, RevisionData, RevisionRecord

# Register your models here.
admin.site.register(MaterialType)
admin.site.register(StandardPpe)
admin.site.register(Manufacturer)
admin.site.register(LifetimeOfPpe)
admin.site.register(TypeOfPpe)
admin.site.register(RevisionData)
admin.site.register(RevisionRecord)

