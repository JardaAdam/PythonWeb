
from django.forms import ModelForm


class BaseFileRequirementForm(ModelForm):
    image_field_name = None
    document_field_name = None
    require_files = True  # Defaultně nastavíme, že soubory jsou požadovány

    def clean(self):
        cleaned_data = super().clean()

        # Pouze pokud je nastaveno, že jsou soubory požadovány
        if self.require_files:
            # Kontrola obrazového pole
            if self.image_field_name:
                image_field = cleaned_data.get(self.image_field_name)
                if not image_field:
                    self.add_error(self.image_field_name, f'{self.image_field_name} is required.')

            # Kontrola dokumentového pole
            if self.document_field_name:
                document_field = cleaned_data.get(self.document_field_name)
                if not document_field:
                    self.add_error(self.document_field_name, f'{self.document_field_name} is required.')

        return cleaned_data