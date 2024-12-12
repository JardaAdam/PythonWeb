from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
# from .forms import CalculatorForm
from revisions.models import TypeOfPpe


# def calculator_view(request):
#     type_of_ppe = TypeOfPpe.objects.all()
#
#     if request.method == "POST":
#         form = CalculatorForm(request.POST)
#         if form.is_valid():
#             total_revision_cost = 0
#             for item in type_of_ppe:
#                 quantity = form.cleaned_data[f'quantity_{item.id}']
#                 total_revision_cost += item.price * quantity
#
#             # Zde můžete uložit výsledek nebo přesměrovat uživatele
#             # print(total_revision_cost) jako výpočet celkové ceny
#
#             # Můžete také přesměrovat na stránku s výsledky nebo zpět na stejnou stránku
#             return redirect('calculator')  # Přesměrování na sebe nebo jinou pohled
#     else:
#         form = CalculatorForm()
#
#     return render(request, 'calculator.html', {'form': form, 'type_of_ppe': type_of_ppe})