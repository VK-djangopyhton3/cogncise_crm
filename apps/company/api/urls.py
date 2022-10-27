from django.urls import path

from apps.company.api import views

urlpatterns = [
    path('update-request/', views.update_request, name='update-request'),
    path('add-company/', views.create_company, name='create-company'),
    path('update-company-info/', views.update_company_info, name='update-company-request')
]
