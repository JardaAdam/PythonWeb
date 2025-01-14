from django.contrib import messages
from django.db.models import Q, ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView, CreateView, DeleteView, ListView


class FilterAndSortMixin(ListView):
    default_sort_field = 'id'  # Definovat výchozí tříditelné pole

    def get_search_fields(self):
        return getattr(self, 'search_fields_by_view', [])

    def get_filtered_queryset(self, queryset):
        # Logika filtrování
        query = self.request.GET.get('q')
        if query:
            queries = Q()
            search_fields = self.get_search_fields()
            for field in search_fields:
                queries |= Q(**{f'{field}__icontains': query})
            queryset = queryset.filter(queries).distinct()
        return queryset

    def get_sorted_queryset(self, queryset):
        # Logika řazení
        sort_by = self.request.GET.get('sort_by', self.default_sort_field)
        sort_order = self.request.GET.get('sort_order', 'asc')
        order_field = f"-{sort_by}" if sort_order == 'desc' else sort_by
        return queryset.order_by(order_field)

    def get_queryset(self):
        queryset = super().get_queryset()  # Toto očekává dědictví nebo směsimo do třídy s `get_queryset`
        queryset = self.get_filtered_queryset(queryset)
        queryset = self.get_sorted_queryset(queryset)
        return queryset

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
class CreateMixin(CreateView):
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


class UpdateMixin(UpdateView):
    detail_url_name = ''
    success_message = 'The changes have been successfully uploaded from CreateMixin'
    error_message = ''
    warning_message = ''
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        # Logika přesměrování
        if self.detail_url_name:
            detail_url = reverse(self.detail_url_name, kwargs={'pk': self.object.pk})
            return redirect(detail_url)  # Přesměrování na detaily
        return response  # Vrátí základní response, pokud detail_url není definováno

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, self.error_message)
        return response

    def add_warning_message(self):
        if self.warning_message:
            pass

class DeleteMixin(DeleteView):
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
    # def delete(self, request, *args, **kwargs):
    #     try:
    #         response = super().delete(request, *args, **kwargs)
    #         messages.success(self.request, self.success_message)
    #         return response
    #     except ProtectedError:
    #         # Vytvoření chybové zprávy pro uživatele
    #         messages.error(self.request, self.error_message)
    #
    #         # Získání "referer" URL, pokud neexistuje, přesměruj na seznam
    #         referer = request.META.get('HTTP_REFERER', reverse('manufacturers_list'))
    #         return HttpResponseRedirect(referer)



# todo doplnit pole pro zobrazovani spravy o uspesnem smazani
