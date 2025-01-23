from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from django.views import View

from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404

from accounts.mixins import LoggerMixin
from revisions.mixins import SearchSortMixin, DeleteMixin, ManySearchSortMixin
from .forms import  SecurityQuestionForm, PasswordResetForm, UserRegistrationForm, CompanyForm, CustomUserUpdateForm, ItemGroupForm
from .models import Company, CustomUser, ItemGroup
from revisions.models import RevisionRecord


User = get_user_model()
# TODO skontrolovat vsechny preklady do Aj !!
# Create your views here.
""" Custom User"""

class ContactView(TemplateView):
    template_name = 'contact.html'


def forgot_password_view(request):
    if request.method == "POST":
        form = SecurityQuestionForm(request.POST)
        if form.is_valid():
            user = get_user_model()
            username = form.cleaned_data['username']
            user = user.objects.get(username__iexact=username)
            return redirect('password_reset', user_id=user.id)
    else:
        form = SecurityQuestionForm()

    return render(request, 'account_form.html', {'form': form})

def password_reset_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password successfully reset. You can now login with your new password.")
            return redirect('login')
    else:
        form = PasswordResetForm()

    return render(request, 'account_form.html', {'form': form})
class UserRegisterView(View):
    # TODO nastavit vychozi hodnotu pro Groups permision
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
    # FIXME Busines ID a Tax id upravit hodnotu prazdneho zapisu na jinou nez None
    """Edit user data"""
    model = CustomUser
    form_class = CustomUserUpdateForm
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

class CompanyListView(LoginRequiredMixin, SearchSortMixin, ListView):
    """ only for revision technician"""
    # TODO upravit vyhledavani tak aby nebyl problem s velkym a malim pismenem
    # TODO kde se bude tato tabulka zobrazovat?
    # FIXME tato tabulka je pouze pro revision technic a admin
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

# Fixme upravit podminky podle prav uzivatele. pro cesty


class CompanyView(LoginRequiredMixin, TemplateView):
    # TODO doresit tento pohled a co se v nem bude zobrazovat myslenka je takova ze tady bude mit uzivatel moznost
    #  videt sve kolegi ve firme a item_group firmy
    #  company view (pro uzivatele z firmy)
    # FIXME nezobrazuje se Last update
    """View solely for the user assigned to the company"""
    model = Company
    form_class = CompanyForm
    template_name = 'my_company.html'
    success_url = reverse_lazy('my_company')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.company:
            context['company'] = self.request.user.company
            context['can_edit'] = self.request.user.groups.filter(name='CompanySupervisor').exists()
        else:
            context['company'] = None
            context['no_company_message'] = "No company assigned."
        return context

class CompanyDetailView(LoginRequiredMixin, DetailView):
    # TODO company detail (pro revizni techniky)
    # TODO doplnit do template created_by a Updated By
    model = Company
    template_name = 'company_detail.html'
    context_object_name = 'company'

class CompanyCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    """ Muze vytvaret pouze CompanySupervisor"""
    model = Company
    form_class = CompanyForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        # Zkontroluje, zda je uživatel ve skupině 'Company Supervisor'
        return self.request.user.groups.filter(name='CompanySupervisor').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Add Company'
        return context


    def form_valid(self, form):
        # Uložíme společnost bez commitu, abychom mohli přidat uživatele
        company = form.save(commit=False)
        company.created_by = self.request.user  # Můžeš upravit podle potřeby (pokud máš např. pole manager)
        company.save()

        # Aktualizujeme uživatele, aby se přidělil k nově vytvořené společnosti
        self.request.user.company = company
        self.request.user.save()

        messages.success(self.request, 'Company added successfully and you have been assigned to it.')
        return super().form_valid(form)

class CompanyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, LoggerMixin):
    """ Muze upravovat pouze CompanySupervisor"""
    model = Company
    form_class = CompanyForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('my_company')


    def test_func(self):
        # Zkontroluje, zda je uživatel ve skupině 'Company Supervisor'
        return self.request.user.groups.filter(name='CompanySupervisor').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Edit Company'
        return context

    def get_success_url(self):
        # Získání hodnoty next parametru z GET/POST požadavku
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url:
            return next_url
        return super().get_success_url()

    def form_valid(self, form):
        # Zaznamená aktuálního uživatele jako toho, kdo aktualizoval záznam
        company = form.save(commit=False)
        company.updated_by = self.request.user
        company.save()

        messages.success(self.request, 'Company updated successfully.')
        response = super().form_valid(form)
        return response

    def handle_no_permission(self):
        self.log_warning(f"Unauthorized access attempt by user ID {self.request.user.id}")
        return super().handle_no_permission()

class CompanyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteMixin, DeleteView):
    # TODO muze pouze Admin (Superuser)
    model = Company
    template_name = 'account_delete.html'
    success_url = reverse_lazy('profile')


""" ItemGroup """

class ItemGroupUserListView(LoginRequiredMixin, ManySearchSortMixin, ListView):
    model = ItemGroup
    template_name = 'user_item_group_list.html'
    context_object_name = 'user_item_groups'

    search_fields = {
        'item_group': ['name', 'user__first_name', 'user__last_name', 'company__name', 'created', 'updated'],
        'revision_record': [
            'revision_data__lifetime_of_ppe__manufacturer__name',
            'revision_data__lifetime_of_ppe__material_type__name',
            'revision_data__type_of_ppe__group_type_ppe',
            'revision_data__name_ppe',
            'serial_number',
            'verdict',
        ],
    }

    def get_queryset(self):
        queryset = ItemGroup.objects.filter(user=self.request.user).annotate(
            record_count=Count('revision_record')
        )
        queryset = self.filter_queryset(queryset, self.search_fields['item_group'])
        queryset = self.sort_queryset(queryset, table_id='user_items', default_sort_field='name')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        free_revision_records = RevisionRecord.objects.filter(owner=self.request.user, item_group=None)
        free_revision_records = self.filter_queryset(free_revision_records, self.search_fields['revision_record'])
        free_revision_records = self.sort_queryset(free_revision_records, table_id='free_records',
                                                   default_sort_field='serial_number')

        context['user_free_revision_records'] = free_revision_records
        context['title'] = 'User Item Groups'
        return context

class ItemGroupCompanyListView(LoginRequiredMixin, ManySearchSortMixin, ListView):
    """View pro firemni uceli"""
    model = ItemGroup
    template_name = 'company_item_group_list.html'
    context_object_name = 'company_item_groups'

    search_fields = {
        'item_group': ['name', 'user__first_name', 'user__last_name', 'company__name', 'created', 'updated'],
        'revision_record': [
            'revision_data__lifetime_of_ppe__manufacturer__name',
            'revision_data__lifetime_of_ppe__material_type__name',
            'revision_data__type_of_ppe__group_type_ppe',
            'revision_data__name_ppe',
            'serial_number',
            'verdict',
        ],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_queryset(queryset, self.search_fields['item_group'])

        # Filtruje ItemGroups podle společnosti uživatele
        if self.request.user.company:
            queryset = queryset.filter(company=self.request.user.company).annotate(
                record_count=Count('revision_record')
            )
        else:
            queryset = queryset.none()  # Žádné záznamy, pokud uživatel nemá společnost
        queryset = self.sort_queryset(queryset, table_id='company_items', default_sort_field='name')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        company_users = User.objects.filter(company=self.request.user.company)
        free_revision_records = RevisionRecord.objects.filter(owner__in=company_users, item_group=None)

        free_revision_records = self.filter_queryset(free_revision_records, self.search_fields['revision_record'])
        free_revision_records = self.sort_queryset(free_revision_records, table_id='free_records',
                                                   default_sort_field='serial_number')

        context['company_free_revision_records'] = free_revision_records
        context['title'] = 'Company Item Groups'
        return context


class ItemGroupDetailView(LoginRequiredMixin,SearchSortMixin, DetailView):

    # TODO doresit upravy dat ze strany uzivatele. ? udelat si formular ktery bude mit zpristupneny uzivatel
    #  a formular v revisions nechat pouze pro revizni techniky?,
    # TODO doplnit vyhledavani podle : Date of Manufacture,Date of First Use, Date of Revision
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




class ItemGroupCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # TODO pri vytvareni Itemgroup chci podminit podle uzivatelskeho opravneni ze
    #  uzivatel muze pridat skupinu ktera patri pouze jemu
    # FIXME pro CompanySupervisor upravit nastaveni omezit Queryset pro users a defaultne nastavit Company
    model = ItemGroup
    form_class = ItemGroupForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        allowed_groups = ['CompanyUser', 'CompanySupervisor', 'RevisionTechnician']
        return any(self.request.user.groups.filter(name=group).exists() for group in allowed_groups)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.groups.filter(name='CompanyUser').exists():
            kwargs['user'] = self.request.user
            kwargs['company'] = self.request.user.company
        return kwargs


    # Formulář inicializujeme s kontrolou a automatickým nastavením společnosti
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields.pop('created_by', None)
        form.fields.pop('updated_by', None)
        if 'user' in form.fields and self.request.user.groups.filter(name='CompanyUser').exists():
            form.instance.user = self.request.user
            form.instance.company = self.request.user.company
            form.fields.pop('user', None)
            form.fields.pop('company', None)
        return form


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Add Item Group'
        return context

    def form_valid(self, form):
        item_group = form.save(commit=False)
        item_group.created_by = self.request.user
        item_group.save()
        messages.success(self.request, 'Item Group was successfully created.')
        return super().form_valid(form)


    def get_success_url(self):
        # Přesměrovat uživatele na detail nově vytvořené ItemGroup
        return reverse('item_group_detail', kwargs={'pk': self.object.pk})

class ItemGroupUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # TODO uzivatel muze upravit pouze skupinu ktera patri jemu
    model = ItemGroup
    form_class = ItemGroupForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('item_group_user_list')

    def test_func(self):
        allowed_groups = ['CompanyUser', 'CompanySupervisor', 'RevisionTechnician']
        is_in_allowed_group = any(self.request.user.groups.filter(name=group).exists() for group in allowed_groups)

        # Získání instace item group pro porovnání
        item_group = self.get_object()

        # Kontrola, zda je uživatel vlastníkem ItemGroup (CompanyUser)
        is_owner = item_group.user == self.request.user

        # Kontrola, zda je uživatel CompanySupervisor pro stejnou společnost jako ItemGroup
        is_supervisor_for_company = (
                self.request.user.groups.filter(name='CompanySupervisor').exists() and
                item_group.company == self.request.user.company
        )

        # Uživateli je povoleno editovat, pokud splňuje podmínky na úrovni skupiny a buď je vlastníkem,
        # nebo je správcem pro svou společnost
        return is_in_allowed_group and (is_owner or is_supervisor_for_company)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.groups.filter(name='CompanyUser').exists():
            kwargs['user'] = self.request.user
            kwargs['company'] = self.request.user.company
        return kwargs

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        form.fields.pop('created_by', None)
        form.fields.pop('updated_by', None)

        # Nastavení povinného pole company na základě uživatele
        form.instance.company = self.request.user.company

        # Nastavit povolená pole pro různé uživatelské role
        if self.request.user.groups.filter(name='CompanyUser').exists():
            form.instance.user = self.request.user
            allowed_fields = ['name']
        elif self.request.user.groups.filter(name='CompanySupervisor').exists():
            allowed_fields = ['user', 'name']
            form.fields['user'].queryset = CustomUser.objects.filter(company=self.request.user.company)
        else:
            # Pokud není ve specifických skupinách, nedovolovat žádné pole k úpravě
            allowed_fields = []

        # Všechna pole, která nejsou ve allowed_fields, bude zakázána
        for field_name in list(form.fields):
            if field_name not in allowed_fields:
                form.fields[field_name].disabled = True

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Update Item Group'
        return context


    def form_valid(self, form):
        item_group = form.save(commit=False)
        item_group.updated_by = self.request.user
        item_group.save()
        messages.success(self.request, 'Item Group was successfully updated.')
        return super().form_valid(form)

    def get_success_url(self):
        # Zajistí, že přesměrujeme na detailní pohled s `pk` aktuálního záznamu
        return reverse('item_group_detail', kwargs={'pk': self.object.pk})

class ItemGroupDeleteView(LoginRequiredMixin, DeleteMixin, DeleteView): # UserPassesTestMixin,
    # FIXME presmerovat podle stranky ze ktere jsem prisel.
    model = ItemGroup
    template_name = 'account_delete.html'
    success_url = reverse_lazy('profile')

    # def test_func(self):
    #     allowed_groups = ['CompanyUser', 'CompanySupervisor', 'RevisionTechnician']
    #     return any(self.request.user.groups.filter(name=group).exists() for group in allowed_groups)


class SubmittableLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('login_success')

    def get_success_url(self):
        return self.success_url

class LoginSuccessView(TemplateView):
    template_name = 'login_success.html'