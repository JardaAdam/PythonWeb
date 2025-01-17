from django.core.exceptions import ValidationError
from django.forms import ModelForm



class BaseFileRequirementForm:
    image_field_name = None
    document_field_name = None

    def clean(self):
        cleaned_data = super().clean()

        # Check for image field
        if self.image_field_name:
            image_field = cleaned_data.get(self.image_field_name)
            if not image_field:
                # Add error to the specific image field
                self.add_error(self.image_field_name, f'{self.image_field_name} is required.')

        # Check for document field
        if self.document_field_name:
            document_field = cleaned_data.get(self.document_field_name)
            if not document_field:
                # Add error to the specific document field
                self.add_error(self.document_field_name, f'{self.document_field_name} is required.')

        return cleaned_data