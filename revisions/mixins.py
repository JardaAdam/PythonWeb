from django.contrib import messages
from django.db.models import Q, ProtectedError
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView, CreateView, DeleteView, ListView


class QuerysetFilterMixin(ListView):
    search_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()  # super() by mělo cílít na třídu, která má metodu get_queryset
        query = self.request.GET.get('q')  # self.request předpokládá, že třída, která používá tento mixin, dědí od View
        if query:
            queries = Q()
            for field in self.search_fields:
                queries |= Q(**{f'{field}__icontains': query})
            queryset = queryset.filter(queries)
        return queryset

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
            messages.error(self.request, self.error_message)
        return response

    def add_warning_message(self):
        if self.warning_message:
            messages.warning(self.request, self.warning_message)


class UpdateMixin(UpdateView):
    detail_url_name = ''
    success_message = 'The changes have been successfully saved from CreateMixin'
    error_message = ''
    warning_message = ''
# TODO doplnit message pole do template _detail.html doresit kde se sprava zobrazuje
    def form_valid(self, form):
        response = super().form_valid(form)
        # Vyhodnocení URL pro detailní zobrazení na základě `detail_url_name`
        if self.detail_url_name:
            detail_url = reverse(self.detail_url_name, kwargs={'pk': self.object.pk})
            # Nastav hlášku o úspěchu
            messages.success(self.request, self.success_message)
            # Přesměruj uživatele na detailní zobrazení
            return redirect(detail_url)

    def form_invalid(self, form):
        pass
    def add_warning_message(self):
        if self.warning_message:
            pass

class DeleteMixin(DeleteView):
    success_message = 'The item was successfully deleted.'
    error_message = 'This item cannot be deleted because it is protected.'


# todo doplnit pole pro zobrazovani spravy o uspesnem smazani
