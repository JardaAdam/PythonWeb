import logging
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404

from accounts.mixins import LoggerMixin
from revisions.mixins import SearchSortMixin, DeleteMixin, UpdateMixin, CreateMixin
from .forms import  SecurityQuestionForm, PasswordResetForm, UserRegistrationForm, CompanyForm, CustomUserUpdateForm, ItemGroupForm
from .models import Company, CustomUser, ItemGroup
from revisions.models import RevisionRecord

# logger = logging.getLogger(__name__)

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
    # TODO muze vytvaret uzivatel Company Supervisor
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
    # TODO muze vytvaret uzivatel Company Supervisor
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

class CompanyDeleteView(LoginRequiredMixin, DeleteMixin, DeleteView):
    # TODO muze pouze Admin (Superuser)
    model = Company
    template_name = 'account_delete.html'
    success_url = reverse_lazy('profile')


""" ItemGroup """

class ItemGroupListView(LoginRequiredMixin, SearchSortMixin, ListView):
    # FIXME pro revisionTechnician a SuperUser chci videt vsechny ItemGroups, vsechny free_revision_records
    # FIXME upravit tak aby kazde searh pole hledalo ve sve casti Template.
    # TODO pridat funkci ktera oznaci vice polozek revision record ktere nemaji ItemGroup a zmenim jejich umisteni do urcite ItemGroup
    model = ItemGroup
    template_name = 'item_group_list.html'
    context_object_name = 'item_groups'
    default_sort_field = 'name'
    search_fields_by_view = ['name', 'user__first_name', 'user__last_name', 'company__name', 'created', 'updated'
                             ]

    def get_queryset(self):
        queryset = super().get_queryset()
        """ zobrazeni uzivatelovich item groups"""

        # Filtrujeme podle aktuálního uživatele, aby viděli pouze své ItemGroups
        queryset = queryset.filter(user=self.request.user)

        # Použití zbytku logiky pro filtrování a řazení pomocí mixinu
        queryset = self.filter_queryset(queryset)
        queryset = self.sort_queryset(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """ data pro zobrazeni revision record ktere nemaji ImemGroup """

        # Přidání volných RevisionRecords do kontextu
        free_revision_records = RevisionRecord.objects.filter(owner=self.request.user, item_group=None)

        context['free_revision_records'] = free_revision_records
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
    # TODO uzivatel muze upravit pouze skupinu ktera patri jemu
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

class ItemGroupDeleteView(LoginRequiredMixin, DeleteMixin, DeleteView):
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