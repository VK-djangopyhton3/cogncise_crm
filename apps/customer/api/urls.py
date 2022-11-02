from django.urls import path

from apps.customer.api import views

urlpatterns = [
    path('add-customer/', views.add_customer, name='add-customer'),
    path('search-customer', views.CustomerListSearch.as_view(), name='search-customer'),
    path('update-sms-consent/', views.sms_consent_update, name='update-sms-consent')
]
