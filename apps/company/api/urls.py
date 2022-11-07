from django.urls import path

from apps.company.api import views

urlpatterns = [
    path('request-company-info-update/', views.update_request, name='update-request'),
    path('add-company/', views.create_company, name='create-company'),
    path('company-info-update-approval/', views.update_company_info, name='update-company-request'),
    path('company-search', views.CompanySearchList.as_view(), name='update-company-request'),
    path('company-delete/', views.delete_company, name='update-company-request'),
    path('company-details/', views.company_details, name='update-company-request')
]
