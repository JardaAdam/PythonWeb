import logging
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404

from revisions.mixins import FilterAndSortMixin
from .forms import UserRegistrationForm, CompanyForm, UserEditForm, ItemGroupForm
from .models import Company, CustomUser, ItemGroup
from revisions.models import RevisionRecord

logger = logging.getLogger(__name__)

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

    @transaction.atomic
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

    @transaction.atomic
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
class CompanyListView(LoginRequiredMixin, FilterAndSortMixin, ListView):
    model = Company
    template_name = 'company_list.html'
    context_object_name = 'companies'
    paginate_by = 10
    search_fields_by_view = ['name', 'country__name', 'city', 'business_id']

    # TODO upravit vyhledavani tak aby nebyl problem s velkym a malim pismenem

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

    @transaction.atomic
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

    @transaction.atomic
    def form_valid(self, form):
        messages.success(self.request, 'Company was successfully updated.')
        return super().form_valid(form)

class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'account_delete.html'
    success_url = reverse_lazy('profile')


""" ItemGroup """
# TODO pri vytvareni Itemgroup chci podminit podle uzivatelskeho opravneni ze
# uzivatel muze pridat skupinu ktera patri pouze jemu
class ItemGroupListView(LoginRequiredMixin, FilterAndSortMixin, ListView):
    model = ItemGroup
    template_name = 'item_group_list.html'
    context_object_name = 'item_groups'
    search_fields_by_view = ['name', 'user__first_name', 'user__last_name', 'company__name', 'created', 'updated']

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = ItemGroup.objects.all()
        else:
            queryset = ItemGroup.objects.filter(user=self.request.user)

        return self.get_filtered_queryset(self.get_sorted_queryset(queryset))

class ItemGroupDetailView(LoginRequiredMixin, DetailView):
    # TODO doresit jak se bude zobrazovat tento detail jestli bude zobrazovat polozky a jak se v nich bude filtrovat
    model = ItemGroup
    template_name = 'item_group_detail.html'
    context_object_name = 'item_group'



class ItemGroupCreateView(LoginRequiredMixin, CreateView):
    model = ItemGroup
    form_class = ItemGroupForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('item_group_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Add PPE Group'
        return context

    @transaction.atomic
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

    @transaction.atomic
    def form_valid(self, form):
        messages.success(self.request, 'Item Group was successfully updated.')
        return super().form_valid(form)

class ItemGroupDeleteView(LoginRequiredMixin, DeleteView):
    model = ItemGroup
    template_name = 'account_delete.html'
    success_url = reverse_lazy('item_group_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Item Group was successfully deleted.')
        return super().delete(request, *args, **kwargs)

class SubmittableLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('login_success')

    def get_success_url(self):
        return self.success_url

class LoginSuccessView(TemplateView):
    template_name = 'login_success.html'