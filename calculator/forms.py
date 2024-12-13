
# from revisions.models import TypeOfPpe

# class CalculatorForm(forms.Form):
"""dynamicky generovaná pole pro každou položku. Uživatelé budou moci upravit pouze pole `quantity`."""
#     def __init__(self, *args, **kwargs):
#         super(CalculatorForm, self).__init__(*args, **kwargs)
#         ppe_items = TypeOfPpe.objects.all()
#         for item in ppe_items:
#             # Dynamicky přidat pole pro každou položku
#             self.fields[f'quantity_{item.id}'] = forms.IntegerField(
#                 min_value=0,
#                 initial=0,
#                 label=item.group_type_ppe
#             )

