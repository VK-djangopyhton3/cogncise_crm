from django.urls import path

from apps.customer.api import views

urlpatterns = [
    path('add-customer/', views.CustomerViews.as_view(), name='add-customer'),
    path('update-customer/', views.CustomerViews.as_view(), name='update-customer'),
    path('search-customer', views.CustomerListSearch.as_view(), name='search-customer'),
]
