from django.contrib.auth import login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from .forms import SignUpForm
from django.views.generic import TemplateView


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
