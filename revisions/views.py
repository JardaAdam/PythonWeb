from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from .forms import MaterialTypeForm, StandardPpeForm, ManufacturerForm, TypeOfPpeForm, RevisionDataForm, \
    RevisionRecordForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def some_view(request):
    return render(request, 'revision_home.html')

@login_required
# Tento dekorátor zajistí, že pohled je přístupný jen přihlášeným uživatelům.
#@permission_required('app_name.change_modelname', raise_exception=True)
#Tento dekorátor se používá k ověření, zda má uživatel konkrétní oprávnění.
def add_data(request):
    form = None
    # Získání hodnoty model_type z GET parametrů; výchozí je 'RevisionRecord'
    model_type = request.GET.get('model_type', 'RevisionRecord')

    if request.method == 'POST':
        # Získání model_type z POST, což určuje, který formulář má být zpracován
        model_type = request.POST.get('model_type')

        # Podmíněné vytvoření formuláře na základě model_type
        if model_type == 'MaterialType':
            form = MaterialTypeForm(request.POST)
        elif model_type == 'StandardPpe':
            form = StandardPpeForm(request.POST)
        elif model_type == 'Manufacturer':
            form = ManufacturerForm(request.POST)
        elif model_type == 'TypeOfPpe':
            form = TypeOfPpeForm(request.POST)
        elif model_type == 'RevisionData':
            form = RevisionDataForm(request.POST)
        elif model_type == 'RevisionRecord':
            form = RevisionRecordForm(request.POST)

        if form.is_valid():
            # Zvláštní ošetření pro formulář RevisionRecord, kdy se musí doplnit created_by
            if model_type == 'RevisionRecord':
                revision_record = form.save(commit=False)  # Uložíme data, ale neprovádíme commit do DB
                revision_record.created_by = request.user   # Nastavujeme aktuálního uživatele
                revision_record.save()                      # Teď uložíme do DB
            else:
                form.save()

            # Přesměrování zpět na stejný typ formuláře po uložení
            return redirect(f"{reverse('add_data')}?model_type={model_type}")

    else:
        # Inicializace prázdného formuláře na základě model_type
        if model_type == 'MaterialType':
            form = MaterialTypeForm()
        elif model_type == 'StandardPpe':
            form = StandardPpeForm()
        elif model_type == 'Manufacturer':
            form = ManufacturerForm()
        elif model_type == 'TypeOfPpe':
            form = TypeOfPpeForm()
        elif model_type == 'RevisionData':
            form = RevisionDataForm()
        elif model_type == 'RevisionRecord':
            form = RevisionRecordForm()

    context = {
        'form': form,             # Připravený formulář, který bude zobrazen v šabloně
        'model_type': model_type  # Model type pro určení výběru ve formuláři nebo po přesměrování
    }

    # Renderování šablony add_data.html s kontextem obsahujícím formulář a model_type
    return render(request, 'add_data.html', context)


def get_form(request):
    model_type = request.GET.get('model_type')

    if model_type == 'MaterialType':
        form = MaterialTypeForm()
    elif model_type == 'StandardPpe':
        form = StandardPpeForm()
    elif model_type == 'Manufacturer':
        form = ManufacturerForm()
    elif model_type == 'TypeOfPpe':
        form = TypeOfPpeForm()
    elif model_type == 'RevisionData':
        form = RevisionDataForm()
    elif model_type == 'RevisionRecord':
        form = RevisionRecordForm()
    else:
        form = None

    context = {
        'form': form
    }

    html = render_to_string('form_partial.html', context)
    return HttpResponse(html)

# def create_revision_record(request):
#     if request.method == 'POST':
#         form = RevisionRecordForm(request.POST)
#         if form.is_valid():
#             revision_record = form.save(commit=False)
#             revision_record.created_by = request.user  # Nastavení aktuálního uživatele jako tvůrce
#             revision_record.save()
#             return redirect('some-success-url')
#         else:
#             # zpracování chyb
#             pass
#     else:
#         form = RevisionRecordForm()
#
#     return render(request, 'template.html', {'form': form})
