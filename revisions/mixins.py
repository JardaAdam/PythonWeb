import os
from django.contrib import messages
from django.db.models import Q, ProtectedError, FileField, ImageField
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView, CreateView, DeleteView


# TODO vyhledávání dat které maji háčky a čárky je case sensitive !
class SearchSortMixin:
    default_sort_field = 'id'  # Výchozí tříditelné pole

    def get_search_fields(self):
        return getattr(self, 'search_fields_by_view', [])

    def filter_queryset(self, queryset):
        if not hasattr(self, 'request'):
            raise AttributeError(
                "Instance nemá atribut 'request', SearchSortMixin musí být použit ve třídách s 'request' atributem.")

        query = self.request.GET.get('q')
        if query:
            queries = Q()
            search_fields = self.get_search_fields()
            for field in search_fields:
                # Použití `__icontains` pro filtrování náchylné na případnosti
                queries |= Q(**{f'{field}__icontains': query})
            queryset = queryset.filter(queries).distinct()
        return queryset

    def sort_queryset(self, queryset):
        sort_by = self.request.GET.get('sort_by', self.default_sort_field)
        sort_order = self.request.GET.get('sort_order', 'asc')
        order_field = f"-{sort_by}" if sort_order == 'desc' else sort_by
        return queryset.order_by(order_field)

# class QuerysetFilterMixin(ListView):
#     search_fields = []
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         query = self.request.GET.get('q')
#         if query:
#             queries = Q()
#             for field in self.search_fields:
#                 queries |= Q(**{f'{field}__icontains': query})
#             queryset = queryset.filter(queries).distinct()
#         return queryset
"""- Buď si vědom, že použití `distinct()` může ovlivnit výkon, zvláště pokud máš rozsáhlé tabulky a komplexní vazby.

- Pokud uvidíš problémy s výkonem nebo složitější chování z důvodu použití `ManyToManyField`, 
může být nutné optimalizovat databázové vztahy nebo přístup k datům jinými způsoby, jako použití `prefetch_related`.

Tento přístup ti umožní zpracovávat `ManyToManyField` v rámci vyhledávání bez opakování položek, 
což by mělo řešit tvůj aktuální problém s duplicitními výsledky při filtrování."""
# TODO po odladeni sprav po premeni spravi tady musim upravit spravi i v testech
class CreateMixin():
    success_message = 'The item was successfully saved from CreateMixin'
    error_message = 'error message from CreateMixin'
    warning_message = 'warning message from CreateMixin'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        messages.success(self.request, self.success_message)
        # Zůstaňte na současné stránce, obnovením stejného formuláře (metoda GET)
        return redirect(self.request.path)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.error_message:
            # Přidejte ladicí zprávy pro chyby formuláře
            print("Form Errors:", form.errors)
            messages.error(self.request, self.error_message)
        return response

    def add_warning_message(self):
        if self.warning_message:
            messages.warning(self.request, self.warning_message)


class UpdateMixin():
    detail_url_name = ''
    success_message = 'The changes have been successfully uploaded from UpdateMixin'
    error_message = ''
    warning_message = ''

    def form_valid(self, form):
        self.object = form.save(commit=False)

        # Uložení starých souborů pro porovnání před uložením nových dat
        old_files = {
            field.name: getattr(self.object, field.name)
            for field in self.object._meta.fields
            if isinstance(field, (FileField, ImageField))  # Ujistěte se, že ImageField je pokryt
        }

        response = super().form_valid(form)  # Uložení nového objektu, zatím smazání starých souborů

        # Porovnat a smazat staré soubory, pokud byly nahrazeny
        for field_name, old_file in old_files.items():
            new_file = getattr(self.object, field_name)
            if old_file and old_file != new_file:
                old_file_path = old_file.path
                if os.path.isfile(old_file_path):
                    os.remove(old_file_path)

        messages.success(self.request, self.success_message)

        if self.detail_url_name:
            detail_url = reverse(self.detail_url_name, kwargs={'pk': self.object.pk})
            return redirect(detail_url)

        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, self.error_message)
        return response

    def add_warning_message(self):
        if self.warning_message:
            messages.warning(self.request, self.warning_message)

class DeleteMixin():
    success_message = 'The item was successfully deleted.'
    error_message = 'This item cannot be deleted because it is protected and has associated records.'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, self.success_message)
        except ProtectedError:
            messages.error(self.request, self.error_message)
        return HttpResponseRedirect(success_url)





