from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from .forms import MaterialTypeForm, StandardPpeForm, ManufacturerForm, TypeOfPpeForm, RevisionDataForm, \
    RevisionRecordForm, LifetimeOfPpeForm
from .models import MaterialType, StandardPpe, Manufacturer, LifetimeOfPpe, TypeOfPpe, RevisionData, RevisionRecord


def home(request):
    return render(request, 'home.html')


def some_view(request):
    return render(request, 'revision_home.html')

# TODO sjednotit guery sety a form_valid pokud to pujde
# TODO ukladani dat je vporadku. doplnit informacni hlasku ze ulozeni probehlo vporadku nebo ze nebylo ulozeno protoze...
# TODO osetrit vypisi v situacich kdy nemuze uzivatel udelat nejaky ukon. ProtectedError atd.
""" Standart PPE"""


class StandardPpeListView(ListView):
    model = StandardPpe
    template_name = 'standard_ppe_list.html'
    context_object_name = 'standards_ppe'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(code__icontains=query) |
                Q(description__icontains=query)
            )
        return queryset


class StandardPpeDetailView(DetailView):
    model = StandardPpe
    template_name = 'standard_ppe_detail.html'
    context_object_name = 'standard_ppe'


class StandardPpeCreateView(CreateView):
    model = StandardPpe
    form_class = StandardPpeForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('standard_ppe_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Získání URL z parametru 'next'
        next_url = self.request.GET.get('next', self.success_url)
        # Pokud 'next' není k dispozici, použijeme success_url nebo defaultní link

        return redirect(next_url)


class StandardPpeUpdateView(UpdateView):
    model = StandardPpe
    form_class = StandardPpeForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('standard_ppe_list')


class StandardPpeDeleteView(DetailView):
    model = StandardPpe
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('standard_ppe_list')


"""Manufacturer"""


class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = 'manufacturer_list.html'
    context_object_name = 'manufacturers'
    success_url = reverse_lazy('manufacturer_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
            )
        return queryset


class ManufacturerDetailView(DetailView):
    model = Manufacturer
    template_name = 'manufacturer_detail.html'
    context_object_name = 'manufacturer'


class ManufacturerCreateView(CreateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('manufacturer_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Získání URL z parametru 'next'
        next_url = self.request.GET.get('next', self.success_url)
        # Pokud 'next' není k dispozici, použijeme success_url nebo defaultní link

        return redirect(next_url)


class ManufacturerUpdateView(UpdateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('manufacturer_list')


class ManufacturerDeleteView(DeleteView):
    model = Manufacturer
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('manufacturer_list')


"""Lifetime Of Ppe"""


class LifetimeOfPpeListView(ListView):
    model = LifetimeOfPpe
    template_name = 'lifetime_of_ppe_list.html'
    context_object_name = 'lifetimes_of_ppe'
    success_url = reverse_lazy('lifetime_of_ppe_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(manufacturer__name__icontains=query) |
                Q(material_type__name__icontains=query) |
                Q(lifetime_use_years__icontains=query) |
                Q(lifetime_manufacture_years__icontains=query)
            )
        return queryset


class LifetimeOfPpeDetailView(DetailView):
    model = LifetimeOfPpe
    template_name = 'lifetime_of_ppe_detail.html'
    context_object_name = 'lifetime_of_ppe'


class LifetimeOfPpeCreateView(CreateView):
    model = LifetimeOfPpe
    form_class = LifetimeOfPpeForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('lifetime_of_ppe_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Získání URL z parametru 'next'
        next_url = self.request.GET.get('next', self.success_url)
        # Pokud 'next' není k dispozici, použijeme success_url nebo defaultní link

        return redirect(next_url)


class LifetimeOfPpeUpdateView(UpdateView):
    model = LifetimeOfPpe
    form_class = LifetimeOfPpeForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('lifetimes_of_ppe_list')


class LifetimeOfPpeDeleteView(DeleteView):
    model = LifetimeOfPpe
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('lifetimes_of_ppe_list')


"""Type Of Ppe"""

""" Revision data"""


class RevisionDataListView(ListView):
    model = RevisionData
    template_name = 'revision_data_list.html'
    context_object_name = 'revisions_data'
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
    template_name = 'revision_data_detail.html'
    context_object_name = 'revision_data'


class RevisionDataCreateView(CreateView):
    model = RevisionData
    form_class = RevisionDataForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('add_revision_data')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Získání URL z parametru 'next'
        next_url = self.request.GET.get('next', self.success_url)
        # Pokud 'next' není k dispozici, použijeme success_url nebo defaultní link

        return redirect(next_url)


class RevisionDataUpdateView(UpdateView):
    model = RevisionData
    form_class = RevisionDataForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('revision_data_list')


class RevisionDataDeleteView(DeleteView):
    model = RevisionData
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('revision_data_list')


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
    template_name = 'revision_record_detail.html'
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
    success_url = reverse_lazy('revision_record_list')


class RevisionRecordDeleteView(DeleteView):
    model = RevisionRecord
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('revision_records_list')

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
