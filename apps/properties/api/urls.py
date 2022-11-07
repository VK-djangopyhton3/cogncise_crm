from django.urls import path

from apps.properties.api import views

urlpatterns = [
    path('add-property-type/', views.create_property_type, name='add-property-type'),
    path('update-property-type/', views.update_property_type, name='update-property-type'),
    path('delete-property-type/', views.delete_property_type, name='delete-property-type'),
    path('search-property-type', views.PropertyTypeSearchList.as_view(), name='search-property-type'),
    path('add-property/', views.property_add, name='add-property'),
    path('property-details', views.property_details, name='property-details'),
    path('search-property', views.PropertySearchList.as_view(), name='search-property'),
    path('delete-property/', views.delete_property, name='delete-property'),
    path('update-property/', views.update_property, name='update-property'),
]
