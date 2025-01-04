from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from .forms import MaterialTypeForm, StandardPpeForm, ManufacturerForm, TypeOfPpeForm, RevisionDataForm, \
    RevisionRecordForm, LifetimeOfPpeForm
from .models import MaterialType, StandardPpe, Manufacturer,LifetimeOfPpe, TypeOfPpe, RevisionData, RevisionRecord


def home(request):
    return render(request, 'home.html')


def some_view(request):
    return render(request, 'revision_home.html')
# TODO predelat zobrazovani a definovat kazdy model zvlast!!
# TODO ukladani dat je vporadku. zobrazovani se musi upravit tak aby se dal v kazdem modelu pridavat a mazat

"""Lifetime Of Ppe"""

"""Type Of Ppe"""

""" Revision data"""

class RevisionDataListView(ListView):
    model = RevisionData
    template_name = 'revision_data_list.html'
    context_object_name = 'revision_data'
    success_url = reverse_lazy('revision_home')

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name_ppe__icontains=query) |
                Q(lifetime_of_ppe__manufacturer__name__icontains=query) |
                Q(group_type_ppe__group_type_ppe__icontains=query)
                # Přidat další pole nebo logiku filtrování podle potřeby
            )
        return queryset


class RevisionDataDetailView(DetailView):
    model = RevisionData
    template_name = 'revision_detail.html'
    context_object_name = 'revision_data'


class RevisionDataCreateView(CreateView):
    model = RevisionData
    form_class = RevisionDataForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('add_revision_data')
    def form_valid(self, form):
        response = super().form_valid(form)
        # Získání URL z parametru 'next'
        next_url = self.request.GET.get('next', '')
        # Pokud 'next' není k dispozici, použijeme success_url nebo defaultní link
        return redirect(next_url or self.success_url)
class RevisionDataUpdateView(UpdateView):
    model = RevisionData
    template_name = 'revision_form.html'
    success_url = reverse_lazy('revision_home')

""" Revision records"""
class RevisionRecordListView(ListView):
    model = RevisionRecord
    template_name = 'revision_record_list.html'
    context_object_name = 'revision_records'
    """Vyhledavani v zaznamech """
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(serial_number__icontains=query) |
                Q(revision_data__lifetime_of_ppe__manufacturer__name__icontains=query) |
                Q(revision_data__group_type_ppe__group_type_ppe__icontains=query) |
                Q(revision_data__name_ppe__icontains=query)
            )
        return queryset

class RevisionRecordDetailView(DetailView):
    model = RevisionRecord
    template_name = 'revision_detail.html'
    context_object_name = 'revision_record'

# TODO tato funkce bude slouzit pro uzivatele ktery bude moci pridat pouze novy vyrobek!!!
class RevisionRecordCreateView(CreateView):
    model = RevisionRecord
    form_class = RevisionRecordForm
    template_name = 'revision_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        messages.success(self.request, "The item was successfully saved")
        # Zůstaňte na současné stránce, obnovením stejného formuláře (metoda GET)
        return redirect(self.request.path)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Nastavení podmínky, kdy tlačítko má být viditelné
        context['show_add_revision_data_button'] = True
        return context

class RevisionRecordUpdateView(UpdateView):
    model = RevisionRecord
    form_class = RevisionRecordForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('revision_home')


class RevisionRecordDeleteView(DeleteView):
    model = RevisionRecord
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('revision_home')



@login_required
def add_data(request):
    form = None
    model_type = request.GET.get('model_type', 'RevisionRecord')

    if request.method == 'POST':
        model_type = request.POST.get('model_type')

        # Ověření, zda model_type existuje a je platný
        if model_type == 'MaterialType':
            form = MaterialTypeForm(request.POST, request.FILES)
        elif model_type == 'StandardPpe':
            form = StandardPpeForm(request.POST, request.FILES)
        elif model_type == 'Manufacturer':
            form = ManufacturerForm(request.POST, request.FILES)
        elif model_type == 'LifetimeOfPpe':
            form = LifetimeOfPpeForm(request.POST)
        elif model_type == 'TypeOfPpe':
            form = TypeOfPpeForm(request.POST, request.FILES)
        elif model_type == 'RevisionData':
            form = RevisionDataForm(request.POST, request.FILES)
        elif model_type == 'RevisionRecord':
            form = RevisionRecordForm(request.POST, request.FILES)

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
        elif model_type == 'LifetimeOfPpe':
            form = LifetimeOfPpeForm()
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
    elif model_type == 'LifetimeOfPpe':
        form = LifetimeOfPpeForm()
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
