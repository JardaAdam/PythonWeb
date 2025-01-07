from django.urls import path
from .views import *

urlpatterns = [
    path('', some_view, name='revision_home'),

    path('standards_ppe/', StandardPpeListView.as_view(), name='standard_ppe_list'),
    path('standard_ppe/<int:pk>/', StandardPpeDetailView.as_view(), name='standard_ppe_detail'),
    path('standard_ppe/add/', StandardPpeCreateView.as_view(), name='add_standard_ppe'),
    path('standard_ppe/edit/<int:pk>/', StandardPpeUpdateView.as_view(), name='edit_standard_ppe'),
    path('standard_ppe/delete/<int:pk>', StandardPpeDeleteView.as_view(), name='delete_standard_ppe'),

    path('manufacturers/', ManufacturerListView.as_view(), name='manufacturer_list'),
    path('manufacturer/<int:pk>/', ManufacturerDetailView.as_view(), name='manufacturer_detail'),
    path('manufacturer/add/', ManufacturerCreateView.as_view(), name='add_manufacturer'),
    path('manufacturer/edit/<int:pk>/', ManufacturerUpdateView.as_view(), name='edit_manufacturer'),
    path('manufacturer/delete/<int:pk>/', ManufacturerDeleteView.as_view(), name='delete_manufacturer'),

    path('lifetimes_of_ppe/', LifetimeOfPpeListView.as_view(), name='lifetimes_of_ppe_list'),
    path('lifetime_of_ppe/<int:pk>/', LifetimeOfPpeDetailView.as_view(), name='lifetime_of_ppe_detail' ),
    path('lifetime_of_ppe/add/', LifetimeOfPpeCreateView.as_view(), name='add_lifetime_of_ppe'),
    path('lifetime_of_ppe/edit/<int:pk>/', LifetimeOfPpeUpdateView.as_view(), name='edit_lifetime_of_ppe'),
    path('lifetime_of_ppe/delete/<int:pk>', LifetimeOfPpeDeleteView.as_view(), name='delete_lifetime_of_ppe'),

    path('records/', RevisionRecordListView.as_view(), name='revision_record_list'),
    path('record/<int:pk>/', RevisionRecordDetailView.as_view(), name='revision_record_detail'),
    path('record/add/', RevisionRecordCreateView.as_view(), name='add_revision_record'),
    path('record/edit/<int:pk>/', RevisionRecordUpdateView.as_view(), name='edit_revision_record'),
    path('record/delete/<int:pk>/', RevisionRecordDeleteView.as_view(), name='delete_revision_record'),

    path('revision_data/', RevisionDataListView.as_view(), name='revision_data_list'),
    path('revision/<int:pk>/', RevisionDataDetailView.as_view(), name='revision_data_detail'),
    path('revision_data/add/', RevisionDataCreateView.as_view(), name='add_revision_data'),
    path('revision_data/edit/<int:pk>/', RevisionDataUpdateView.as_view(), name='edit_revision_data'),
    path('revision_data/delete/<int:pk>/', RevisionDataDeleteView.as_view(), name='delete_revision_data'),



]