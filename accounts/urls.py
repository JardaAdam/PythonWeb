from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import SubmittableLoginView, LoginSuccessView, UserRegisterView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),  # defaultní cesty a views z Djanga
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', SubmittableLoginView.as_view(), name='login'),
    path('login/success/', LoginSuccessView.as_view(), name='login_success'),
    # path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
