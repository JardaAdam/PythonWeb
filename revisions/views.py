from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import MaterialTypeForm, StandardPpeForm, ManufacturerForm, TypeOfPpeForm, RevisionDataForm, \
    RevisionRecordForm
from .models import MaterialType, StandardPpe, Manufacturer, TypeOfPpe, RevisionData, RevisionRecord


def home(request):
    return render(request, 'home.html')


def some_view(request):
    return render(request, 'revision_home.html')
# TODO predelat zobrazovani a definovat kazdy model zvlast!!
# TODO ukladani dat je vporadku. zobrazovani se musi upravit tak aby se dal v kazdem modelu pridavat a mazat
# TODO pohrat si s navbarem a revision_home.html
@login_required
def view_data(request):
    model_type = request.GET.get('model_type', 'RevisionRecord')
    form = None
    data = None

    if model_type == 'MaterialType':
        data = MaterialType.objects.all()
        form = MaterialTypeForm()
    elif model_type == 'StandardPpe':
        data = StandardPpe.objects.all()
        form = StandardPpeForm()
    elif model_type == 'Manufacturer':
        data = Manufacturer.objects.all()
        form = ManufacturerForm()
    elif model_type == 'TypeOfPpe':
        data = TypeOfPpe.objects.all()
        form = TypeOfPpeForm()
    elif model_type == 'RevisionData':
        data = RevisionData.objects.all()
        form = RevisionDataForm()
    elif model_type == 'RevisionRecord':
        data = RevisionRecord.objects.all()
        form = RevisionRecordForm()

    context = {
        'data': data,
        'form': form,
        'model_type': model_type,
    }
    return render(request, 'view_data.html', context)

@login_required
def add_data(request):
    form = None
    model_type = request.GET.get('model_type', 'RevisionRecord')

    if request.method == 'POST':
        model_type = request.POST.get('model_type')

        # Ověření, zda model_type existuje a je platný
        if model_type == 'MaterialType':
            form = MaterialTypeForm(request.POST)
        elif model_type == 'StandardPpe':
            form = StandardPpeForm(request.POST, request.FILES)
        elif model_type == 'Manufacturer':
            form = ManufacturerForm(request.POST)
        elif model_type == 'TypeOfPpe':
            form = TypeOfPpeForm(request.POST, request.FILES)
        elif model_type == 'RevisionData':
            form = RevisionDataForm(request.POST, request.FILES)
        elif model_type == 'RevisionRecord':
            form = RevisionRecordForm(request.POST)

        if form is not None and form.is_valid():
            if model_type == 'RevisionRecord':
                revision_record = form.save(commit=False)
                revision_record.created_by = request.user
                revision_record.save()
            else:
                form.save()

            messages.success(request, 'The item was successfully saved.')
            return redirect(f"{reverse('add_data')}?model_type={model_type}")

    # Inicializace formuláře při GET požadavku nebo při nevalidním POST
    if form is None:
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
        'form': form,
        'model_type': model_type,
    }
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

    context = {'form': form}
    html = render_to_string('form_partial.html', context, request=request)
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
