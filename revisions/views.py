from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from .mixins import SearchSortMixin, CreateMixin, UpdateMixin, DeleteMixin

from .forms import MaterialTypeForm, StandardPpeForm, ManufacturerForm, TypeOfPpeForm, RevisionDataForm, \
    RevisionRecordForm, LifetimeOfPpeForm

from .models import MaterialType, StandardPpe, Manufacturer, LifetimeOfPpe, TypeOfPpe, RevisionData, RevisionRecord


def home(request):
    return render(request, 'home.html')


def some_view(request):
    return render(request, 'revision_home.html')
# TODO doplnit do templates rozkliknuti fotek
# TODO kontrola kam se ukladaji soubory
# TODO do revision_form.html doplnit kolonku pro zobrazovani aktualniho pridavaneho form
# TODO pokud to pujde tak pro jednoduzsi listy sjednotit Template do jednoho
# TODO ukladani dat je vporadku. doplnit informacni hlasku ze ulozeni probehlo vporadku nebo ze nebylo ulozeno protoze...
# TODO osetrit vypisi v situacich kdy nemuze uzivatel udelat nejaky ukon. ProtectedError atd.
# TODO doplnit listovani do vsech Template_list (paginate_by = 10), {% include "includes/pagination.html" %}
# TODO doplnit pro create a update context_data pro view_title
# TODO upravit kdy se uzivateli zobrazuje search field v revision_base.html pouze v ListView
""" MaterialType """

class MaterialTypeListView(SearchSortMixin,ListView):
    model = MaterialType
    template_name = 'materials_type_list.html'
    context_object_name = 'materials_type'
    success_url = reverse_lazy('revision_home')
    default_sort_field = 'name'
    search_fields_by_view = ['id','name']


    def get_queryset(self):
        # Získáme původní queryset definovaný modelem
        queryset = super().get_queryset()

        # Filtrujeme data podle vstupu uživatele
        queryset = self.filter_queryset(queryset)

        # Řadíme data podle uživatelského vstupu nebo výchozí verze
        queryset = self.sort_queryset(queryset)

        return queryset
class MaterialTypeDetailView(DetailView):
    model = MaterialType
    template_name = 'material_type_detail.html'
    context_object_name = 'material_type'
    success_url = reverse_lazy('materials_type_list')

class MaterialTypeCreateView(LoginRequiredMixin,CreateMixin, CreateView):
    model = MaterialType
    form_class = MaterialTypeForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('materials_type_list')

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     form.save()
    #     messages.success(self.request, "The item was successfully saved")
    #     # Zůstaňte na současné stránce, obnovením stejného formuláře (metoda GET)
    #     return redirect(self.request.path)

class MaterialTypeUpdateView(LoginRequiredMixin,UpdateMixin, UpdateView):
    model = MaterialType
    form_class = MaterialTypeForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('materials_type_list')
    detail_url_name = 'material_type_detail'
    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     # Získej URL pro detailní zobrazení upraveného záznamu
    #     detail_url = reverse('material_type_detail', kwargs={'pk': self.object.pk})
    #     # Nastav hlášku o úspěchu
    #     messages.success(self.request, "The changes have been successfully saved")
    #     # Přesměruj uživatele na detailní zobrazení
    #     return redirect(detail_url)
class MaterialTypeDeleteView(LoginRequiredMixin, DeleteMixin, DeleteView):
    model = MaterialType
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('materials_type_list')

""" Standart PPE"""


class StandardPpeListView(SearchSortMixin,ListView):
    # FIXME dolatit template tak aby nadpis byl na stredu
    model = StandardPpe
    template_name = 'standard_ppe_list.html'
    context_object_name = 'standards_ppe'
    success_url = reverse_lazy('revision_home')
    default_sort_field = 'code'
    search_fields_by_view = ['code', 'description']
      # Zvolte jedno, které je smysluplné pro váš případ

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.sort_queryset(queryset)

        return queryset


class StandardPpeDetailView(DetailView):
    model = StandardPpe
    template_name = 'standard_ppe_detail.html'
    context_object_name = 'standard_ppe'
    success_url = reverse_lazy('standards_ppe_list')

class StandardPpeCreateView(LoginRequiredMixin,CreateMixin, CreateView):
    model = StandardPpe
    form_class = StandardPpeForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('standards_ppe_list')

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     form.save()
    #     messages.success(self.request, "The item was successfully saved")
    #     # Zůstaňte na současné stránce, obnovením stejného formuláře (metoda GET)
    #     return redirect(self.request.path)


class StandardPpeUpdateView(LoginRequiredMixin,UpdateMixin, UpdateView):
    model = StandardPpe
    form_class = StandardPpeForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('standards_ppe_list')
    detail_url_name = 'standard_ppe_detail'

class StandardPpeDeleteView(LoginRequiredMixin,DeleteMixin, DeleteView):
    model = StandardPpe
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('standards_ppe_list')


"""Manufacturer"""


class ManufacturerListView(SearchSortMixin,ListView):
    model = Manufacturer
    template_name = 'manufacturer_list.html'
    context_object_name = 'manufacturers'
    success_url = reverse_lazy('revision_home')
    default_sort_field = 'name'
    search_fields_by_view = ['name']


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.sort_queryset(queryset)

        return queryset


class ManufacturerDetailView(DetailView):
    model = Manufacturer
    template_name = 'manufacturer_detail.html'
    context_object_name = 'manufacturer'


class ManufacturerCreateView(LoginRequiredMixin,CreateMixin, CreateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('manufacturers_list')

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     form.save()
    #     messages.success(self.request, "The item was successfully saved")
    #     # Zůstaňte na současné stránce, obnovením stejného formuláře (metoda GET)
    #     return redirect(self.request.path)


class ManufacturerUpdateView(LoginRequiredMixin,UpdateMixin, UpdateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('manufacturers_list')
    detail_url_name = 'manufacturer_detail'


class ManufacturerDeleteView(LoginRequiredMixin, DeleteMixin, DeleteView):
    model = Manufacturer
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('manufacturers_list')


"""Lifetime Of Ppe"""


class LifetimeOfPpeListView(SearchSortMixin,ListView):
    model = LifetimeOfPpe
    template_name = 'lifetime_of_ppe_list.html'
    context_object_name = 'lifetimes_of_ppe'
    success_url = reverse_lazy('revision_home')
    default_sort_field = 'manufacturer__name'
    search_fields_by_view = ['manufacturer__name','material_type__name',
                             'lifetime_use_years',
                             'lifetime_manufacture_years']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.sort_queryset(queryset)

        return queryset


class LifetimeOfPpeDetailView(DetailView):
    model = LifetimeOfPpe
    template_name = 'lifetime_of_ppe_detail.html'
    context_object_name = 'lifetime_of_ppe'


class LifetimeOfPpeCreateView(LoginRequiredMixin,CreateMixin, CreateView):
    model = LifetimeOfPpe
    form_class = LifetimeOfPpeForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('lifetimes_of_ppe_list')

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     form.save()
    #     messages.success(self.request, "The item was successfully saved")
    #     # Zůstaňte na současné stránce, obnovením stejného formuláře (metoda GET)
    #     return redirect(self.request.path)


class LifetimeOfPpeUpdateView(LoginRequiredMixin,UpdateMixin, UpdateView):
    model = LifetimeOfPpe
    form_class = LifetimeOfPpeForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('lifetimes_of_ppe_list')
    detail_url_name = 'lifetime_of_ppe_detail'


class LifetimeOfPpeDeleteView(LoginRequiredMixin,DeleteMixin, DeleteView):
    model = LifetimeOfPpe
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('lifetimes_of_ppe_list')


"""Type Of Ppe"""

class TypeOfPpeListView(SearchSortMixin,ListView):
    model = TypeOfPpe
    template_name = 'type_of_ppe_list.html'
    context_object_name = 'types_of_ppe'
    success_url = reverse_lazy('revision_home')
    default_sort_field = 'group_type_ppe'
    search_fields_by_view = ['group_type_ppe','price']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.sort_queryset(queryset)

        return queryset
class TypeOfPpeDetailView(DetailView):
    model = TypeOfPpe
    template_name = 'type_of_ppe_detail.html'
    context_object_name = 'type_of_ppe'

class TypeOfPpeCreateView(LoginRequiredMixin,CreateMixin, CreateView):
    model = TypeOfPpe
    form_class = TypeOfPpeForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('types_of_ppe_list')

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     form.save()
    #     messages.success(self.request, "The item was successfully saved")
    #     # Zůstaňte na současné stránce, obnovením stejného formuláře (metoda GET)
    #     return redirect(self.request.path)

class TypeOfPpeUpdateView(LoginRequiredMixin,UpdateMixin, UpdateView):
    model = TypeOfPpe
    form_class = TypeOfPpeForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('types_of_ppe_list')
    detail_url_name = 'type_of_ppe_detail'

class TypeOfPpeDeleteView(LoginRequiredMixin,DeleteMixin, DeleteView):
    model = TypeOfPpe
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('types_of_ppe_list')


""" Revision data"""


class RevisionDataListView(SearchSortMixin,ListView):
    model = RevisionData
    paginate_by = 10
    template_name = 'revision_data_list.html'
    context_object_name = 'revisions_data'
    success_url = reverse_lazy('revision_home')
    default_sort_field = 'name_ppe'
    search_fields_by_view = ['lifetime_of_ppe__manufacturer__name',
                             'lifetime_of_ppe__material_type__name',
                             'type_of_ppe__group_type_ppe',
                             'type_of_ppe__price',
                             'name_ppe',
                             'standard_ppe__code',
                             'standard_ppe__description']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.sort_queryset(queryset)

        return queryset

class RevisionDataDetailView(DetailView):
    model = RevisionData
    template_name = 'revision_data_detail.html'
    context_object_name = 'revision_data'


class RevisionDataCreateView(LoginRequiredMixin,CreateMixin, CreateView):
    model = RevisionData
    form_class = RevisionDataForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('revision_datas_list')

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     form.save()
    #     messages.success(self.request, "The item was successfully saved")
    #     # Zůstaňte na současné stránce, obnovením stejného formuláře (metoda GET)
    #     return redirect(self.request.path)


class RevisionDataUpdateView(LoginRequiredMixin,UpdateMixin, UpdateView):
    model = RevisionData
    form_class = RevisionDataForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('revision_datas_list')
    detail_url_name = 'revision_data_detail'

class RevisionDataDeleteView(LoginRequiredMixin,DeleteMixin, DeleteView):
    model = RevisionData
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('revision_datas_list')


""" Revision records"""


# TODO Item group do teto template ma prijit jeste zobrazeni pro pridani nove skupiny, odkaz na vytvoreni nove,
#  pridavani jednotlivich prvku do skupin
#  zobrazovani prvku podle skupiny do ktere patri
#  zobrazeni dle owner
# TODO pri zvoleni new pri update se zobrazi ulozeni probehlo vporadku ale zaznam se nezmeni
#
class RevisionRecordListView(LoginRequiredMixin,SearchSortMixin,ListView):
    # FIXME doplnit vyhledavani podle itemgroup a owner, date of manufacture......
    model = RevisionRecord
    paginate_by = 10
    template_name = 'revision_record_list.html'
    context_object_name = 'revision_records'
    success_url = reverse_lazy('revision_home')
    default_sort_field = 'revision_data__name_ppe'
    search_fields_by_view = ['revision_data__lifetime_of_ppe__manufacturer__name',
                             'revision_data__lifetime_of_ppe__material_type__name',
                             'revision_data__type_of_ppe__group_type_ppe',
                             'revision_data__name_ppe',
                             'serial_number',
                             'verdict']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.sort_queryset(queryset)

        return queryset



class RevisionRecordDetailView(LoginRequiredMixin,DetailView):
    # TODO zobrazovat i forku z revision data
    # FIXME Doplnit owner do detail view
    model = RevisionRecord
    template_name = 'revision_record_detail.html'
    context_object_name = 'revision_record'



class RevisionRecordCreateView(LoginRequiredMixin,CreateMixin, CreateView):
    # FIXME Upravit zobrazovani chyb ve formulari
    # FIXME sort by created date
    model = RevisionRecord
    form_class = RevisionRecordForm
    template_name = 'revision_form.html'

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     form.save()
    #     messages.success(self.request, "The item was successfully saved")
    #     # Zůstaňte na současné stránce, obnovením stejného formuláře (metoda GET)
    #     return redirect(self.request.path)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Nastavení podmínky, kdy tlačítko má být viditelné
        context['show_add_revision_data_button'] = True
        return context

# TODO tato funkce bude slouzit pro uzivatele ktery bude moci pridat pouze novy vyrobek!!!
class RevisionRecordCreateViewByOwner(LoginRequiredMixin,CreateMixin, CreateView):
    # TODO pridat funkci pro pridavani zaznamu uzivatelem: automaticke nastaveni owner a zadani pouze new.
    pass

class RevisionRecordUpdateView(LoginRequiredMixin,UpdateMixin, UpdateView):
    model = RevisionRecord
    form_class = RevisionRecordForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('revision_records_list')
    detail_url_name = 'revision_record_detail'

class RevisionRecordUpdateViewByOwner(LoginRequiredMixin,UpdateView):
    #TODO pridat pohled pro pridani uzivatelem mozne upravi: zmena a pridani ItemGroup, pridani poznamky a foto_of_item
    pass



class RevisionRecordDeleteView(LoginRequiredMixin,DeleteMixin, DeleteView):
    model = RevisionRecord
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('revision_records_list')


