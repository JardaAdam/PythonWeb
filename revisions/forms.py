from django.forms import ModelForm, Select
from django.forms.widgets import SelectMultiple

from .models import MaterialType, StandardPpe, Manufacturer, LifetimeOfPpe, TypeOfPpe, RevisionData, RevisionRecord
# TODO doplnit vyhledavaci widgets
# TODO doplnit napovedu pro spravny format poli
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

class LifetimeOfPpeForm(ModelForm):
    class Meta:
        model = LifetimeOfPpe
        fields = '__all__'

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
            'group_type_ppe': Select(attrs={'class': 'form-control select2'}),
            'standard_ppe': SelectMultiple(attrs={'class': 'form-control select2'}),
        }
# TODO doplnit napovedu pro spravny format poli
class RevisionRecordForm(ModelForm):
    class Meta:
        model = RevisionRecord
        fields = '__all__'
        exclude = ['created_by']
        widgets = {
            'revision_data': Select(attrs={'class': 'form-control select2'}),
        }
