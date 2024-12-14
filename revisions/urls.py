from django.urls import path
from . import views

urlpatterns = [
    path('', views.some_view, name='revision_home'),
    path('add/', views.add_data, name='add_data'),
    path('get_form/', views.get_form, name='get_form'),
]