from django.urls import path

from apps.leads.api import views

urlpatterns =[
    path('add-property-type/', views.create_work_type, name='add-property-type'),
    path('update-property-type/', views.update_work_type, name='update-property-type'),
    path('delete-property-type/', views.delete_work_type, name='delete-property-type'),
    path('search-property-type', views.WorkTypeSearchList.as_view(), name='search-property-type'),
]