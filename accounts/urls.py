from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import SubmittableLoginView, LoginSuccessView, UserRegisterView, CompanyCreateView, CustomUserView, \
    CustomUserUpdateView, CompanyUpdateView, CompanyDeleteView, ItemGroupCreateView, \
    ItemGroupUpdateView, \
    ItemGroupDeleteView, CompanyView, CompanyListView, CompanyDetailView, ItemGroupDetailView, forgot_password_view, \
    password_reset_view, ItemGroupCompanyListView, ItemGroupUserListView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),  # defaultní cesty a views z Djanga
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', SubmittableLoginView.as_view(), name='login'),
    path('login/success/', LoginSuccessView.as_view(), name='login_success'),
    # path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('profile/', CustomUserView.as_view(), name='profile'),
    path('profile/edit/', CustomUserUpdateView.as_view(), name='edit_profile'),

    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('company/', CompanyView.as_view(), name='company_view'),
    path('company/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    path('company/add/', CompanyCreateView.as_view(), name='add_company'),
    path('company/edit/<int:pk>/', CompanyUpdateView.as_view(), name='edit_company'),
    path('company/delete/<int:pk>/', CompanyDeleteView.as_view(), name='delete_company'),

    path('item_groups/user/', ItemGroupUserListView.as_view(), name='item_group_user_list'),
    path('item_groups/company/', ItemGroupCompanyListView.as_view(), name='item_group_company_list'),
    path('item_group/<int:pk>/', ItemGroupDetailView.as_view(), name='item_group_detail'),
    path('item_group/add/', ItemGroupCreateView.as_view(), name='add_item_group'),
    path('item_group/edit/<int:pk>/', ItemGroupUpdateView.as_view(), name='edit_item_group'),
    path('item_group/delete/<int:pk>/', ItemGroupDeleteView.as_view(), name='delete_item_group'),

    path('password_change/', auth_views.PasswordChangeView.as_view ,name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='profile.html'), name='password_change_done'),

    path('forgot_password/', forgot_password_view, name='forgot_password'),
    path('password_reset/<int:user_id>/', password_reset_view, name='password_reset'),
]
