from django.urls import path
from .views import *

urlpatterns = [
    path('', some_view, name='revision_home'),
    path('records/', RevisionRecordListView.as_view(), name='revision_list'),
    path('record/<int:pk>/', RevisionRecordDetailView.as_view(), name='revision_detail'),
    path('record/add/', RevisionRecordCreateView.as_view(), name='add_revision'),
    path('record/edit/<int:pk>/', RevisionRecordUpdateView.as_view(), name='edit_revision'),
    path('record/delete/<int:pk>/', RevisionRecordDeleteView.as_view(), name='delete_revision'),

    path('revision_data/', RevisionDataListView.as_view(), name='revision_data'),
    path('revision_data/add/', RevisionDataCreateView.as_view(), name='add_revision_data'),

    path('add/', add_data, name='add_data'),
    path('get_form/', get_form, name='get_form'),
]