from django import forms
from .models import MaterialType, StandardPpe, Manufacturer, TypeOfPpe, RevisionData, RevisionRecord


class MaterialTypeForm(forms.ModelForm):
    class Meta:
        model = MaterialType
        fields = '__all__'


class StandardPpeForm(forms.ModelForm):
    class Meta:
        model = StandardPpe
        fields = '__all__'


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class TypeOfPpeForm(forms.ModelForm):
    class Meta:
        model = TypeOfPpe
        fields = '__all__'


class RevisionDataForm(forms.ModelForm):
    # FIXME upravit formularove data v oblasti Standart ppe aby se nemuselo listovat v okne
    class Meta:
        model = RevisionData
        fields = '__all__'


class RevisionRecordForm(forms.ModelForm):
    class Meta:
        model = RevisionRecord
        fields = '__all__'
        exclude = ['created_by']
