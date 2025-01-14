import logging
from django.db import transaction
from django.db.models import Q
from django.db.utils import IntegrityError
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404

from revisions.mixins import FilterAndSortMixin
from .forms import UserRegistrationForm, CompanyForm, UserEditForm, ItemGroupForm  # ,ItemGroupForm
from .models import Company, CustomUser, ItemGroup

logger = logging.getLogger(__name__)


# Create your views here.
# TODO pouzit transaction Atomic

class UserRegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        user_form = UserRegistrationForm()
        return render(request, self.template_name, {
            'user_form': user_form
        })

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('login_success')

        return render(request, self.template_name, {'user_form': user_form})


class CustomUserView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserEditForm  # Můžete použít stejný formulář, pokud je vhodný.
    template_name = 'account_form.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        # Přidejte dynamické proměnné, které budou použity v šabloně
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Upravit Profil'
        context['button_text'] = 'Uložit'
        return context

    def get_object(self, queryset=None):
        # Zajistěte, aby mohli uživatelé upravit pouze vlastní profil
        return get_object_or_404(CustomUser, pk=self.request.user.pk)

    def form_valid(self, form):
        messages.success(self.request, 'Profil byl úspěšně aktualizován.')
        return super().form_valid(form)


# FIXME omezit uzivateli aby mohl upravovat pouze company do ktere patri
class CompanyListView(LoginRequiredMixin, FilterAndSortMixin, ListView):
    model = Company
    template_name = 'company_list.html'
    context_object_name = 'companies'
    paginate_by = 10  # Počet položek na stránku
    search_fields_by_view = ['name', 'country__name', 'city', 'business_id']

    # TODO upravit vyhledavani tak aby nebyl problem s velkym a malim pismenem
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     query = self.request.GET.get('q')
    #     if query:
    #         queryset = queryset.filter(
    #             Q(name__icontains=query) |
    #             Q(country__name__icontains=query) |
    #             Q(city__icontains=query) |
    #             Q(business_id__icontains=query)
    #         )
    #     return queryset



class CompanyView(LoginRequiredMixin, TemplateView):
    """ View pouze pro uzivatele ktery byl prirazen k firme"""
    model = Company
    form_class = CompanyForm
    template_name = 'company.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Zkontrolujte, zda má aktuální uživatel přiřazenou společnost
        if self.request.user.company:
            context['company'] = self.request.user.company
        else:
            context['company'] = None
            context['no_company_message'] = "Nemáte přiřazenou žádnou společnost."

        return context


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company_detail.html'
    context_object_name = 'company'


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'account_form.html'

    def get_context_data(self, **kwargs):
        # Přidejte dynamické proměnné, které budou použity v šabloně
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Přidat Společnost'
        context['button_text'] = 'Přidat'
        return context

    def form_valid(self, form):
        # Automaticky se postará o validaci a uložení formuláře
        response = super().form_valid(form)
        messages.success(self.request, 'Company added successfully.')
        return response


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'account_form.html'  # Použijte vaši sdílenou šablonu
    success_url = reverse_lazy('profile')  # Kam chcete přesměrovat po úpravě

    def get_context_data(self, **kwargs):
        # Přidejte dynamické proměnné, které budou použity v šabloně
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Upravit Společnost'
        context['button_text'] = 'Uložit'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Společnost byla úspěšně aktualizována.')
        return super().form_valid(form)


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'account_delete.html'
    success_url = reverse_lazy('profile')


# TODO pri vytvareni Itemgroup chci podminit podle uzivatelskeho opravneni ze
#  uzivatel muze pridat skupinu ktera patri pouze jemu
class ItemGroupListView(LoginRequiredMixin, FilterAndSortMixin, ListView):
    model = ItemGroup
    template_name = 'item_group_list.html'
    context_object_name = 'item_groups'
    search_fields_by_view = ['name','user__first_name','user__last_name','company__name','created','updated']

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = ItemGroup.objects.all()
        else:
            queryset = ItemGroup.objects.filter(user=self.request.user)

        return self.get_filtered_queryset(self.get_sorted_queryset(queryset))


class ItemGroupCreateView(LoginRequiredMixin, CreateView):
    model = ItemGroup
    form_class = ItemGroupForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('item_group_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Přidat Skupinu PPE'
        context['button_text'] = 'Přidat'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Item Group byla úspěšně vytvořena.')
        return super().form_valid(form)


class ItemGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = ItemGroup
    form_class = ItemGroupForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('item_group_list')  # Kam přesměrovat po úspěšné úpravě

    def get_context_data(self, **kwargs):
        # Přidejte dynamické proměnné, které budou použity v šabloně
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Upravit Skupinu PPE'
        context['button_text'] = 'Uložit'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Item Group byla úspěšně aktualizována.')
        return super().form_valid(form)


class ItemGroupDeleteView(LoginRequiredMixin, DeleteView):
    model = ItemGroup
    template_name = 'account_delete.html'  # Šablona pro potvrzení smazání
    success_url = reverse_lazy('item_group_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Item Group byla úspěšně smazána.')
        return super().delete(request, *args, **kwargs)
    # def get(self, request):
    #     form = CompanyForm()
    #     return render(request, self.template_name, {'form': form})
    #
    # def post(self, request):
    #     form = CompanyForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Company added successfully.')
    #         return redirect(reverse_lazy('login_success'))  # Nebo jiné místo, kam chcete uživatele přesměrovat
    #     return render(request, self.template_name, {'form': form})


class SubmittableLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('login_success')

    def get_success_url(self):
        return self.success_url


class LoginSuccessView(TemplateView):
    template_name = 'login_success.html'

#
#
#
# def create_item_group(request):
#     if request.method == 'POST':
#         form = ItemGroupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success_url')  # Nahraďte 'success_url' vaší cílovou URL po uložení
#     else:
#         form = ItemGroupForm()
#
#     return render(request, 'item_group_form.html', {'form': form})
