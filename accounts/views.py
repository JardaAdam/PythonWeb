import logging
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404

from revisions.mixins import SearchSortMixin, DeleteMixin
from .forms import UserRegistrationForm, CompanyForm, UserEditForm, ItemGroupForm
from .models import Company, CustomUser, ItemGroup
from revisions.models import RevisionRecord

logger = logging.getLogger(__name__)
# TODO nastavit resset hesla
# TODO skontrolovat vsechny preklady do Aj !!
# Create your views here.
""" Custom User"""
class UserRegisterView(View):
    """User registration"""
    template_name = 'registration/register.html'

    def get(self, request):
        user_form = UserRegistrationForm()
        return render(request, self.template_name, {
            'user_form': user_form
        })

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Save the user instance including password
            user = user_form.save()  # .save() již volá set_password v rámci formy
            login(request, user)
            return redirect('login_success')

        # Pokud form není validní, zobrazí chyby zpět na template
        return render(request, self.template_name, {'user_form': user_form})

class CustomUserView(LoginRequiredMixin, TemplateView):
    """User profile"""
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    """Edit user data"""
    model = CustomUser
    form_class = UserEditForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Edit Profile'
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, pk=self.request.user.pk)


    def form_valid(self, form):
        user = form.save(commit=False)
        # Update the user's company based on form selection
        user.company = form.cleaned_data.get('company')
        user.save()

        messages.success(self.request, 'Profile was successfully updated.')
        print(form.errors)
        return super().form_valid(form)

""" Company """
# FIXME omezit uzivateli aby mohl upravovat pouze company do ktere patri
class CompanyListView(LoginRequiredMixin, SearchSortMixin, ListView):
    # TODO upravit vyhledavani tak aby nebyl problem s velkym a malim pismenem
    model = Company
    template_name = 'company_list.html'
    context_object_name = 'companies'
    paginate_by = 10
    search_fields_by_view = ['name', 'country__name', 'city', 'business_id']
    default_sort_field = 'name'  # Zvolte jedno, které je smysluplné pro váš případ

    def get_queryset(self):
        # Získáme původní queryset definovaný modelem
        queryset = super().get_queryset()

        # Filtrujeme data podle vstupu uživatele
        queryset = self.filter_queryset(queryset)

        # Řadíme data podle uživatelského vstupu nebo výchozí verze
        queryset = self.sort_queryset(queryset)

        return queryset


class CompanyView(LoginRequiredMixin, TemplateView):
    """View solely for the user assigned to the company"""
    model = Company
    form_class = CompanyForm
    template_name = 'company.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.company:
            context['company'] = self.request.user.company
        else:
            context['company'] = None
            context['no_company_message'] = "No company assigned."
        return context

class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company_detail.html'
    context_object_name = 'company'

class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Add Company'
        return context


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Company added successfully.')
        return response

class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Edit Company'
        return context


    def form_valid(self, form):
        messages.success(self.request, 'Company was successfully updated.')
        return super().form_valid(form)

class CompanyDeleteView(LoginRequiredMixin, DeleteMixin):
    model = Company
    template_name = 'account_delete.html'
    success_url = reverse_lazy('profile')


""" ItemGroup """

class ItemGroupListView(LoginRequiredMixin, SearchSortMixin, ListView):
    model = ItemGroup
    template_name = 'item_group_list.html'
    context_object_name = 'item_groups'
    default_sort_field = 'name'
    search_fields_by_view = ['name', 'user__first_name', 'user__last_name', 'company__name', 'created', 'updated']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrujeme podle aktuálního uživatele, aby viděli pouze své ItemGroups
        queryset = queryset.filter(user=self.request.user)

        # Použití zbytku logiky pro filtrování a řazení pomocí mixinu
        queryset = self.filter_queryset(queryset)
        queryset = self.sort_queryset(queryset)
        return queryset

class ItemGroupDetailView(LoginRequiredMixin,SearchSortMixin, DetailView):
    # TODO doresit upravy dat ze strany uzivatele. ? udelat si formular ktery bude mit zpristupneny uzivatel
    #  a formular v revisions nechat pouze pro revizni techniky?,
    # TODO
    model = ItemGroup
    template_name = 'item_group_detail.html'
    context_object_name = 'item_group'
    search_fields_by_view = ['revision_data__lifetime_of_ppe__manufacturer__name',
                             'revision_data__lifetime_of_ppe__material_type__name',
                             'revision_data__type_of_ppe__group_type_ppe',
                             'revision_data__name_ppe',
                             'serial_number',
                             'verdict']
    default_sort_field = 'date_manufacture'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = RevisionRecord.objects.filter(item_group=self.object)
        queryset = self.filter_queryset(queryset)
        queryset = self.sort_queryset(queryset)
        context['revision_records'] = queryset
        context[
            'user_full_name'] = f"{self.object.user.first_name} {self.object.user.last_name}" \
            if self.object.user else "Unknown user"
        return context

class ItemGroupCreateView(LoginRequiredMixin, CreateView):
    # TODO pri vytvareni Itemgroup chci podminit podle uzivatelskeho opravneni ze
    #  uzivatel muze pridat skupinu ktera patri pouze jemu
    model = ItemGroup
    form_class = ItemGroupForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('item_group_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Add PPE Group'
        return context


    def form_valid(self, form):
        messages.success(self.request, 'Item Group was successfully created.')
        return super().form_valid(form)

class ItemGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = ItemGroup
    form_class = ItemGroupForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('item_group_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Edit PPE Group'
        return context


    def form_valid(self, form):
        messages.success(self.request, 'Item Group was successfully updated.')
        return super().form_valid(form)

class ItemGroupDeleteView(LoginRequiredMixin, DeleteMixin):
    model = ItemGroup
    template_name = 'account_delete.html'
    success_url = reverse_lazy('item_group_list')



class SubmittableLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('login_success')

    def get_success_url(self):
        return self.success_url

class LoginSuccessView(TemplateView):
    template_name = 'login_success.html'