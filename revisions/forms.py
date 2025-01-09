from django.forms import ModelForm, Select
from django.forms.widgets import SelectMultiple

from .models import MaterialType, StandardPpe, Manufacturer, LifetimeOfPpe, TypeOfPpe, RevisionData, RevisionRecord
# TODO doplnit napovedu pro spravny format poli
# TODO upravit format zadavani datumu
# TODO clean metody pro zadavani dat



class MaterialTypeForm(ModelForm):
    class Meta:
        model = MaterialType
        fields = '__all__'


class StandardPpeForm(ModelForm):
    class Meta:
        model = StandardPpe
        fields = '__all__'


class ManufacturerForm(ModelForm):
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


class RevisionDataForm(ModelForm):
    class Meta:
        model = RevisionData
        fields = '__all__'
        widgets = {
            'lifetime_of_ppe': Select(attrs={'class': 'form-control select2'}),
            'type_of_ppe': Select(attrs={'class': 'form-control select2'}),
            'standard_ppe': SelectMultiple(attrs={'class': 'form-control select2'}),
        }
# TODO upravit format zadavani datumu

class RevisionRecordForm(ModelForm):
    class Meta:
        model = RevisionRecord
        fields = '__all__'
        exclude = ['created_by']
        widgets = {
            'revision_data': Select(attrs={'class': 'form-control select2'}),
            'item_group': Select(attrs={'class': 'form-control select2'}),
            'owner': Select(attrs={'class': 'form-control select2'}),
        }
