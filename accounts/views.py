from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.urls import reverse_lazy, reverse

from django.views import View

from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404

from accounts.mixins import LoggerMixin, PermissionStaffMixin
from config.mixins import SearchSortMixin, DeleteMixin, ManySearchSortMixin
from .forms import  SecurityQuestionForm, PasswordResetForm, UserRegistrationForm, CompanyForm, CustomUserUpdateForm, ItemGroupForm
from .models import Company, CustomUser, ItemGroup
from revisions.models import RevisionRecord


User = get_user_model()

# Create your views here.
""" Custom User"""
# TODO detail View pro SuperUsera atd.

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
    """User registration
    po registraci uzivatele se pomoci signals.py -> assign_company_supervisor_group
     nastavi vychozi permision Group pro uzivatele"""
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

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        if self.request.user.groups.filter(name='CompanyUser').exists():
            # Skryjte pole company pomocí HiddenInput widgetu
            form.fields['company'].disabled = True  # Disable the field
        return form

    def form_valid(self, form):
        user = form.save(commit=False)
        # Update the user's company based on form selection
        user.company = form.cleaned_data.get('company')
        user.save()

        messages.success(self.request, 'Profile was successfully updated.')
        print(form.errors)
        return super().form_valid(form)

""" Company """

class CompanyListView(PermissionStaffMixin, SearchSortMixin, ListView): # PermissionStaffMixin,
    """ only for revision technician"""
    # TODO upravit vyhledavani tak aby nebyl problem s velkym a malim pismenem
    # TODO kde se bude tato tabulka zobrazovat viditelnost pouze pro SuperUser a RevisionTechnician
    model = Company
    template_name = 'company_list.html'
    context_object_name = 'companies'
    paginate_by = 10
    search_fields_by_view = ['name', 'country__name', 'city', 'business_id']
    default_sort_field = 'name'



    def get_queryset(self):
        # Získáme původní queryset definovaný modelem
        queryset = super().get_queryset()

        # Filtrujeme data podle vstupu uživatele
        queryset = self.filter_queryset(queryset)

        # Řadíme data podle uživatelského vstupu nebo výchozí verze
        queryset = self.sort_queryset(queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



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
            context['can_edit'] = (
                    self.request.user.is_superuser or
                    self.request.user.groups.filter(name='RevisionTechnician').exists() or
                    self.request.user.groups.filter(name='CompanySupervisor').exists()
            )
        else:
            context['company'] = None
            context['no_company_message'] = "No company assigned."
        return context

class CompanyDetailView(PermissionStaffMixin, DetailView):
    # TODO company detail (pro revizni techniky)
    # TODO doplnit do template created_by a Updated By
    # FIXME odkazovat na item group podle company ze ktere prichazim
    model = Company
    template_name = 'company_detail.html'
    context_object_name = 'company'

class CompanyCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    # FIXME pridat create Company Pro SuperUser a RevisionTechnique
    """ Muze vytvaret pouze CompanySupervisor"""
    model = Company
    form_class = CompanyForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='RevisionTechnician').exists():
            return True

        # Uživatelé ve 'CompanySupervisor' mají povolení pouze pokud nemají přiřazenou společnost
        if self.request.user.groups.filter(name='CompanySupervisor').exists() and not self.request.user.company:
            return True
        # Jiní uživatelé nemají povolení
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Add Company'
        return context

    def form_valid(self, form):
        # Uložíme společnost bez commitu, abychom mohli přidat uživatele
        company = form.save(commit=False)
        company.created_by = self.request.user  # uloží aktuálního uživatele
        company.save()

        # Automaticky aktualizujeme uživatele, aby se přidělil k nově vytvořené společnosti
        # pouze pokud je uživatel ve skupině CompanySupervisor
        if self.request.user.groups.filter(name='CompanySupervisor').exists():
            self.request.user.company = company
            self.request.user.save()

        messages.success(self.request, 'Company added successfully.')
        return super().form_valid(form)


    def get_success_url(self):
        # Zjistit, zda je uživatel CompanySupervisor
        if self.request.user.groups.filter(name='CompanySupervisor').exists():
            # Přesměrovat na pohled 'company_view'
            return reverse('company_view')

        # Zjistit, zda je uživatel superuživatel nebo ve skupině 'RevisionTechnician'
        if self.request.user.is_superuser or self.request.user.groups.filter(name='RevisionTechnician').exists():
            # Přesměrovat na detail nově vytvořené společnosti
            return reverse('company_detail', kwargs={'pk': self.object.pk})

        # Pokud by nějaký uživatel nepatřil mezi tyto, vrátíme ho třeba na úvodní stránku
        return reverse('profile')

class CompanyUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView, LoggerMixin):
    """ Muze upravovat pouze CompanySupervisor"""
    model = Company
    form_class = CompanyForm
    template_name = 'account_form.html'


    def test_func(self):
        # Pokud je uživatel superuser nebo 'RevisionTechnician', má přístup bez omezení
        if self.request.user.is_superuser or self.request.user.groups.filter(name='RevisionTechnician').exists():
            return True
        if self.request.user.groups.filter(name='CompanyUser').exists():
            return False
        # Pokud je uživatel ve skupině 'CompanySupervisor', zkontroluj firmu
        if self.request.user.groups.filter(name='CompanySupervisor').exists():
            company = self.get_object()
            return company == self.request.user.company  # Uživatel může měnit pouze svou vlastní firmu

        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Edit Company'
        return context


    def form_valid(self, form):
        # Zaznamená aktuálního uživatele jako toho, kdo aktualizoval záznam
        company = form.save(commit=False)
        company.updated_by = self.request.user
        company.save()

        messages.success(self.request, 'Company updated successfully.')
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        # Získání hodnoty next parametru z GET/POST požadavku
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url:
            return next_url
        return super().get_success_url()

    def handle_no_permission(self):
        self.log_warning(f"Unauthorized access attempt by user ID {self.request.user.id}")
        return super().handle_no_permission()


class CompanyDeleteView(PermissionStaffMixin, DeleteMixin, DeleteView):
    model = Company
    template_name = 'account_delete.html'
    success_url = 'delete_success'
""" ItemGroup """

class ItemGroupUserListView(LoginRequiredMixin, ManySearchSortMixin, ListView):
    model = ItemGroup
    template_name = 'user_item_group_list.html'
    context_object_name = 'user_item_groups'
    paginate_by = 10
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
    paginate_by = 10
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
    # TODO doplnit vyhledavani podle : Date of Manufacture,Date of First Use, Date of Revision
    model = ItemGroup
    template_name = 'item_group_detail.html'
    context_object_name = 'item_group'
    paginate_by = 10
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
    # TODO Pokud vytvari zaznam Superuser nebo RevisionTechnic musi byt pole company povinne
    # TODO doresit testy na zadavani dat superuserem a RevisionTechnicianem
    model = ItemGroup
    form_class = ItemGroupForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        allowed_groups = ['CompanyUser', 'CompanySupervisor', 'RevisionTechnician']
        return any(self.request.user.groups.filter(name=group).exists() for group in allowed_groups)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.user.groups.filter(name='CompanyUser').exists():
            kwargs['user'] = self.request.user
            kwargs['company'] = self.request.user.company
        elif self.request.user.groups.filter(name='CompanySupervisor').exists():
            # Automatické nastavení společnosti pro CompanySupervisor
            kwargs['company'] = self.request.user.company
        elif self.request.user.is_superuser or self.request.user.groups.filter(name='RevisionTechnician').exists():
            # Podmínka pro superusera a RevisionTechnician, kteří by si mohli vybrat společnost
            kwargs['company'] = None  # Nastaveno na None, pokud chcete umožnit výběr společnosti externě
        return kwargs

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        # Pro superuser a RevisionTechnician nastavit pouze určitá pole jako editovatelná
        if self.request.user.is_superuser or self.request.user.groups.filter(name='RevisionTechnician').exists():
            # Zobrazit všechny pole, ale omezit jejich možnosti (např. pomocí disabled)
            for field in form.fields:
                if field not in ['name', 'user', 'company']:
                    form.fields[field].disabled = True

        # Původní logika pro CompanyUser
        if 'user' in form.fields and self.request.user.groups.filter(name='CompanyUser').exists():
            form.instance.user = self.request.user
            form.instance.company = self.request.user.company
            form.fields.pop('user', None)
            form.fields.pop('company', None)
        # Omezení pro CompanySupervisor
        if 'user' in form.fields:
            if self.request.user.groups.filter(name='CompanySupervisor').exists():
                form.fields['user'].queryset = CustomUser.objects.filter(company=self.request.user.company)
                form.instance.company = self.request.user.company
                form.fields.pop('company', None)

        # Vždy odstranit automagické pole
        form.fields.pop('created_by', None)
        form.fields.pop('updated_by', None)


        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Add Item Group'
        return context

    def form_valid(self, form):
        item_group = form.save(commit=False)
        item_group.created_by = self.request.user
        item_group.save()
        messages.success(self.request, 'Item Group was successfully created CreatView.')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Debugování chyb formuláře
        if form.errors:
            print("Form errors:", form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('item_group_detail', kwargs={'pk': self.object.pk})


class ItemGroupUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ItemGroup
    form_class = ItemGroupForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('item_group_user_list')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
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

class ItemGroupDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteMixin, DeleteView, LoggerMixin):
    # FIXME doresit reload stranky ze ktere odesel tak aby zmizel smazany zaznam.
    model = ItemGroup
    template_name = 'account_delete.html'

    def test_func(self):
        item_group = self.get_object()

        # Pokud je uživatel ve skupině 'CompanyUser', může mazat pouze svoje skupiny
        if self.request.user.groups.filter(name='CompanyUser').exists():
            return item_group.user == self.request.user

        # Pokud je uživatel ve skupině 'CompanySupervisor', může mazat všechny skupiny v rámci firmy
        if self.request.user.groups.filter(name='CompanySupervisor').exists():
            return item_group.company == self.request.user.company

        # Pro Superuser nebo RevisionTechnician: mohou mazat všechny skupiny, pokud jsou prázdné
        if self.request.user.is_superuser or self.request.user.groups.filter(name='RevisionTechnician').exists():
            return not item_group.revision_records.exists()  # Vrátí True pouze, pokud neexistují žádné záznamy

        # Ostatní uživatelé nebudou mít přístup
        return False



    def handle_no_permission(self):
        self.log_warning(f"Unauthorized access attempt by user ID {self.request.user.id}")
        return super().handle_no_permission()


class SubmittableLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('login_success')

    def get_success_url(self):
        return self.success_url

class LoginSuccessView(TemplateView):
    template_name = 'login_success.html'