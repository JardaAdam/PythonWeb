from django.forms import ModelForm
from .models import MaterialType, StandardPpe, Manufacturer, TypeOfPpe, RevisionData, RevisionRecord


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


class TypeOfPpeForm(ModelForm):
    class Meta:
        model = TypeOfPpe
        fields = '__all__'


class RevisionDataForm(ModelForm):
    # FIXME upravit formularove data v oblasti Standart ppe aby se nemuselo listovat v okne
    class Meta:
        model = RevisionData
        fields = '__all__'


class RevisionRecordForm(ModelForm):
    class Meta:
        model = RevisionRecord
        fields = '__all__'
        exclude = ['created_by']
