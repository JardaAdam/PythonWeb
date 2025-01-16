from django.forms import ModelForm, Select
from django.forms.widgets import SelectMultiple

from .base_forms import BaseFileRequirementForm
from .models import MaterialType, StandardPpe, Manufacturer, LifetimeOfPpe, TypeOfPpe, RevisionData, RevisionRecord
# TODO doplnit napovedu pro spravny format poli
# TODO upravit format zadavani datumu
# TODO clean metody pro zadavani dat



class MaterialTypeForm(ModelForm):
    class Meta:
        model = MaterialType
        fields = '__all__'


class StandardPpeForm(BaseFileRequirementForm):
    image_field_name = 'image'
    class Meta:
        model = StandardPpe
        fields = '__all__'


class ManufacturerForm(BaseFileRequirementForm):
    image_field_name = 'logo'
    class Meta:
        model = Manufacturer
        fields = '__all__'

# TODO osetrit zadavani delky zivornosti v letech
class LifetimeOfPpeForm(ModelForm):
    class Meta:
        model = LifetimeOfPpe
        fields = '__all__'
        widgets = {
            'manufacturer': Select(attrs={'class': 'form-control select2'}),
            'material_type': Select(attrs={'class': 'form-control select2'}),

        }

class TypeOfPpeForm(ModelForm):
    class Meta:
        model = TypeOfPpe
        fields = '__all__'


class RevisionDataForm(BaseFileRequirementForm):
    image_field_name = 'image_items'
    class Meta:
        model = RevisionData
        fields = '__all__'
        widgets = {
            'lifetime_of_ppe': Select(attrs={'class': 'form-control select2'}),
            'type_of_ppe': Select(attrs={'class': 'form-control select2'}),
            'standard_ppe': SelectMultiple(attrs={'class': 'form-control select2'}),
        }


class RevisionRecordForm(ModelForm):
    # TODO upravit format zadavani datumu
    # FIXME upravit logiku zadavani verdict pole
    class Meta:
        model = RevisionRecord
        fields = '__all__'
        exclude = ['created_by']
        widgets = {
            'revision_data': Select(attrs={'class': 'form-control select2'}),
            'item_group': Select(attrs={'class': 'form-control select2'}),
            'owner': Select(attrs={'class': 'form-control select2'}),
        }
