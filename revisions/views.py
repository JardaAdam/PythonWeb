from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from .mixins import FilterAndSortMixin, CreateMixin, UpdateMixin, DeleteMixin

from .forms import MaterialTypeForm, StandardPpeForm, ManufacturerForm, TypeOfPpeForm, RevisionDataForm, \
    RevisionRecordForm, LifetimeOfPpeForm

from .models import MaterialType, StandardPpe, Manufacturer, LifetimeOfPpe, TypeOfPpe, RevisionData, RevisionRecord


def home(request):
    return render(request, 'home.html')


def some_view(request):
    return render(request, 'revision_home.html')
# TODO zhodnotit jake template jsou lepsi zda ListView nebo TemplateView
# TODO kontrola kam se ukladaji soubory
# TODO do revision_form.html doplnit kolonku pro zobrazovani aktualniho pridavaneho form
# TODO sjednotit guery sety a form_valid pokud to pujde
# TODO ukladani dat je vporadku. doplnit informacni hlasku ze ulozeni probehlo vporadku nebo ze nebylo ulozeno protoze...
# TODO osetrit vypisi v situacich kdy nemuze uzivatel udelat nejaky ukon. ProtectedError atd.
""" MaterialType """

class MaterialTypeListView(FilterAndSortMixin,ListView):
    model = MaterialType
    template_name = 'materials_type_list.html'
    context_object_name = 'materials_type'
    success_url = reverse_lazy('revision_home')
    search_fields_by_view = ['id','name']

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


class StandardPpeListView(FilterAndSortMixin,ListView):
    model = StandardPpe
    template_name = 'standard_ppe_list.html'
    context_object_name = 'standards_ppe'
    success_url = reverse_lazy('revision_home')
    search_fields_by_view = ['code', 'description']

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     query = self.request.GET.get('q')
    #     if query:
    #         queryset = queryset.filter(
    #             Q(code__icontains=query) |
    #             Q(description__icontains=query)
    #         )
    #     return queryset


class StandardPpeDetailView(DetailView):
    model = StandardPpe
    template_name = 'standard_ppe_detail.html'
    context_object_name = 'standard_ppe'
    success_url = reverse_lazy('standards_ppe_list')

class StandardPpeCreateView(LoginRequiredMixin,CreateMixin,CreateView):
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


class StandardPpeUpdateView(LoginRequiredMixin,UpdateMixin,UpdateView):
    model = StandardPpe
    form_class = StandardPpeForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('standards_ppe_list')
    detail_url_name = 'standard_ppe_detail'

class StandardPpeDeleteView(LoginRequiredMixin,DeleteMixin,DeleteView):
    model = StandardPpe
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('standards_ppe_list')


"""Manufacturer"""


class ManufacturerListView(FilterAndSortMixin,ListView):
    model = Manufacturer
    template_name = 'manufacturer_list.html'
    context_object_name = 'manufacturers'
    success_url = reverse_lazy('revision_home')
    search_fields_by_view = ['name']

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     query = self.request.GET.get('q')
    #     if query:
    #         queryset = queryset.filter(
    #             Q(name__icontains=query)
    #         )
    #     return queryset


class ManufacturerDetailView(DetailView):
    model = Manufacturer
    template_name = 'manufacturer_detail.html'
    context_object_name = 'manufacturer'


class ManufacturerCreateView(LoginRequiredMixin,CreateMixin,CreateView):
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


class ManufacturerUpdateView(LoginRequiredMixin,UpdateMixin,UpdateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('manufacturers_list')
    detail_url_name = 'manufacturer_detail'


class ManufacturerDeleteView(LoginRequiredMixin, DeleteMixin, DeleteView):
    model = Manufacturer
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('manufacturers_list')
    #FixME doresit hlaskovou template pro upozorneni ze se nade smazat


"""Lifetime Of Ppe"""


class LifetimeOfPpeListView(FilterAndSortMixin,ListView):
    model = LifetimeOfPpe
    template_name = 'lifetime_of_ppe_list.html'
    context_object_name = 'lifetimes_of_ppe'
    success_url = reverse_lazy('revision_home')
    search_fields_by_view = ['manufacturer__name','material_type__name',
                             'lifetime_use_years',
                             'lifetime_manufacture_years']
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     query = self.request.GET.get('q')
    #     if query:
    #         queryset = queryset.filter(
    #             Q(manufacturer__name__icontains=query) |
    #             Q(material_type__name__icontains=query) |
    #             Q(lifetime_use_years__icontains=query) |
    #             Q(lifetime_manufacture_years__icontains=query)
    #         )
    #     return queryset


class LifetimeOfPpeDetailView(DetailView):
    model = LifetimeOfPpe
    template_name = 'lifetime_of_ppe_detail.html'
    context_object_name = 'lifetime_of_ppe'


class LifetimeOfPpeCreateView(LoginRequiredMixin,CreateMixin,CreateView):
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


class LifetimeOfPpeUpdateView(LoginRequiredMixin,UpdateMixin,UpdateView):
    model = LifetimeOfPpe
    form_class = LifetimeOfPpeForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('lifetimes_of_ppe_list')
    detail_url_name = 'lifetime_of_ppe_detail'


class LifetimeOfPpeDeleteView(LoginRequiredMixin,DeleteMixin,DeleteView):
    model = LifetimeOfPpe
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('lifetimes_of_ppe_list')


"""Type Of Ppe"""

class TypeOfPpeListView(FilterAndSortMixin,ListView):
    model = TypeOfPpe
    template_name = 'type_of_ppe_list.html'
    context_object_name = 'types_of_ppe'
    success_url = reverse_lazy('revision_home')
    search_fields_by_view = ['group_type_ppe','price']
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     query = self.request.GET.get('q')
    #     if query:
    #         queryset = queryset.filter(
    #             Q(group_type_ppe__icontains=query) |  # Vyhledávání podle názvu skupiny
    #             Q(price__icontains=query)  # Vyhledávání podle ceny
    #         )
    #     return queryset
class TypeOfPpeDetailView(DetailView):
    model = TypeOfPpe
    template_name = 'type_of_ppe_detail.html'
    context_object_name = 'type_of_ppe'

class TypeOfPpeCreateView(LoginRequiredMixin,CreateMixin,CreateView):
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

class TypeOfPpeUpdateView(LoginRequiredMixin,UpdateMixin,UpdateView):
    model = TypeOfPpe
    form_class = TypeOfPpeForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('types_of_ppe_list')
    detail_url_name = 'type_of_ppe_detail'

class TypeOfPpeDeleteView(LoginRequiredMixin,DeleteMixin,DeleteView):
    model = TypeOfPpe
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('types_of_ppe_list')


""" Revision data"""


class RevisionDataListView(FilterAndSortMixin,ListView):
    model = RevisionData
    template_name = 'revision_data_list.html'
    context_object_name = 'revisions_data'
    success_url = reverse_lazy('revision_home')
    search_fields_by_view = ['lifetime_of_ppe__manufacturer__name',
                             'lifetime_of_ppe__material_type__name',
                             'type_of_ppe__group_type_ppe',
                             'type_of_ppe__price',
                             'name_ppe',
                             'standard_ppe__code',
                             'standard_ppe__description']

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #
    #     # Zpracování parametrů řazení
    #     sort_by = self.request.GET.get('sort_by', 'id')  # `id` je výchozí pole pro řazení
    #     sort_order = self.request.GET.get('sort_order', 'asc')
    #
    #     # Prepnutí pořadí na sestupné, pokud je potřeba
    #     order_field = f"-{sort_by}" if sort_order == 'desc' else sort_by
    #     queryset = queryset.order_by(order_field)
    #
    #     # Vrátíme se k logice mixinu QuerysetFilterMixin
    #     return queryset

class RevisionDataDetailView(DetailView):
    model = RevisionData
    template_name = 'revision_data_detail.html'
    context_object_name = 'revision_data'


class RevisionDataCreateView(LoginRequiredMixin,CreateMixin,CreateView):
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


class RevisionDataUpdateView(LoginRequiredMixin,UpdateMixin,UpdateView):
    model = RevisionData
    form_class = RevisionDataForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('revision_datas_list')
    detail_url_name = 'revision_data_detail'

class RevisionDataDeleteView(LoginRequiredMixin,DeleteMixin,DeleteView):
    model = RevisionData
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('revision_datas_list')


""" Revision records"""

# TODO doplnit search fields
# TODO Item group do teto template ma prijit jeste zobrazeni pro pridani nove skupiny, odkaz na vytvoreni nove,
#  pridavani jednotlivich prvku do skupin
#  zobrazovani prvku podle skupiny do ktere patri
#  zobrazeni dle owner
# TODO pri zvoleni new pri update se zobrazi ulozeni probehlo vporadku ale zaznam se nezmeni
#
class RevisionRecordListView(LoginRequiredMixin,FilterAndSortMixin,ListView):
    model = RevisionRecord
    template_name = 'revision_record_list.html'
    context_object_name = 'revision_records'
    success_url = reverse_lazy('revision_home')
    search_fields_by_view = ['revision_data__lifetime_of_ppe__manufacturer__name',
                             'revision_data__lifetime_of_ppe__material_type__name',
                             'revision_data__type_of_ppe__group_type_ppe',
                             'revision_data__name_ppe',
                             'serial_number',
                             'verdict']

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #
    #     # Zpracování parametrů řazení
    #     sort_by = self.request.GET.get('sort_by', 'id')  # `id` je výchozí pole pro řazení
    #     sort_order = self.request.GET.get('sort_order', 'asc')
    #
    #     # Prepnutí pořadí na sestupné, pokud je potřeba
    #     order_field = f"-{sort_by}" if sort_order == 'desc' else sort_by
    #     queryset = queryset.order_by(order_field)
    #
    #     # Vrátíme se k logice mixinu QuerysetFilterMixin
    #     return queryset

    # TODO doresit klikaci sortovani



class RevisionRecordDetailView(LoginRequiredMixin,DetailView):
    model = RevisionRecord
    template_name = 'revision_record_detail.html'
    context_object_name = 'revision_record'


# TODO tato funkce bude slouzit pro uzivatele ktery bude moci pridat pouze novy vyrobek!!!

class RevisionRecordCreateView(LoginRequiredMixin,CreateMixin,CreateView):
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


class RevisionRecordUpdateView(LoginRequiredMixin,UpdateMixin,UpdateView):
    model = RevisionRecord
    form_class = RevisionRecordForm
    template_name = 'revision_form.html'
    success_url = reverse_lazy('revision_records_list')
    detail_url_name = 'revision_record_detail'


class RevisionRecordDeleteView(LoginRequiredMixin,DeleteMixin,DeleteView):
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
