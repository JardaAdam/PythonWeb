from django.core.exceptions import ValidationError
from django.forms import ModelForm


class BaseFileRequirementForm(ModelForm):
    image_field_name = None
    document_field_name = None

    def clean(self):
        cleaned_data = super().clean()

        # Check for image field
        if self.image_field_name:
            image_field = cleaned_data.get(self.image_field_name)
            if not image_field:
                raise ValidationError(f'{self.image_field_name} is required.')

        # Check for document field
        if self.document_field_name:
            document_field = cleaned_data.get(self.document_field_name)
            if not document_field:
                raise ValidationError(f'{self.document_field_name} is required.')

        return cleaned_data