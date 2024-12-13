from django.contrib.auth import login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from .forms import SignUpForm
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
# from .forms import ItemGroupForm

# Create your views here.

class SubmittableLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('login_success')

    def get_success_url(self):
        return self.success_url

class LoginSuccessView(TemplateView):
    template_name = 'login_success.html'

class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login_success')

    def form_valid(self, form):
        # Po úspěšné registraci se uživatel přihlásí
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response
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