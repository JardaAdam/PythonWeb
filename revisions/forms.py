from django.forms import ModelForm, Select
from .models import MaterialType, StandardPpe, Manufacturer,LifetimeOfPpe, TypeOfPpe, RevisionData, RevisionRecord


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
            'standard_ppe': Select(attrs={'class': 'form-control select2'}),
        }

class RevisionRecordForm(ModelForm):
    class Meta:
        model = RevisionRecord
        fields = '__all__'
        exclude = ['created_by']
        widgets = {
            'revision_data': Select(attrs={'class': 'form-control select2'}),
        }
