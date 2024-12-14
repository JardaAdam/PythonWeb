from django.db import transaction
from django.db.utils import IntegrityError
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect

from .forms import RegistrationForm, CompanyForm #,ItemGroupForm
from .models import Company


# Create your views here.
class UserRegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        user_form = RegistrationForm()
        company_form = CompanyForm()
        return render(request, self.template_name, {
            'user_form': user_form,
            'company_form': company_form
        })

    def post(self, request):
        user_form = RegistrationForm(request.POST)
        company_form = CompanyForm(request.POST)

        if user_form.is_valid() and (not company_form.has_changed() or company_form.is_valid()):
            try:
                with transaction.atomic():
                    user = user_form.save(commit=False)
                    company = user_form.cleaned_data.get('company')

                    if company:
                        user.company = company
                    elif company_form.cleaned_data:
                        company, created = Company.objects.get_or_create(
                            name=company_form.cleaned_data['name'],
                            defaults=company_form.cleaned_data
                        )
                        user.company = company

                    user.set_password(user_form.cleaned_data['password'])
                    user.save()

                    login(request, user)
                    return redirect('login_success')
            except IntegrityError as e:
                # Přidejte specifickou chybovou zprávu a vypište chybu z integrity error
                user_form.add_error(None, "An error occurred due to data conflicts. Please try adjusting your input.")

                # Debug výstup pro vývojáře
                print(f"IntegrityError: {e}")

        return render(request, self.template_name, {
            'user_form': user_form,
            'company_form': company_form
        })


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