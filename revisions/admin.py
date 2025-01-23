from django.contrib import admin

from revisions.models import MaterialType,StandardPpe, Manufacturer, LifetimeOfPpe, TypeOfPpe, RevisionData, RevisionRecord



class RevisionRecordAdmin(admin.ModelAdmin):
    list_display = ('revision_data_display', 'owner', 'manufacturer', 'serial_number', 'item_group')
    list_filter = ('item_group', 'owner', 'revision_data__lifetime_of_ppe__manufacturer')

    def revision_data_display(self, obj):
        return obj.revision_data.name_ppe

    revision_data_display.short_description = 'PPE Name'

    def manufacturer(self, obj):
        return obj.revision_data.lifetime_of_ppe.manufacturer

    manufacturer.short_description = 'Manufacturer'
# Register your models here.
admin.site.register(MaterialType)
admin.site.register(StandardPpe)
admin.site.register(Manufacturer)
admin.site.register(LifetimeOfPpe)
admin.site.register(TypeOfPpe)
admin.site.register(RevisionData)
admin.site.register(RevisionRecord, RevisionRecordAdmin)

