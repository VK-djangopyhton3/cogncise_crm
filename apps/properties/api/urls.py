from django.urls import path

from apps.properties.api import views

urlpatterns = [
    path('add-property-type/', views.PropertyTypeView.as_view(), name='add-property-type'),
    path('update-property-type/', views.PropertyTypeView.as_view(), name='update-property-type'),
    path('delete-property-type/', views.PropertyTypeView.as_view(), name='delete-property-type'),
    path('search-property-type', views.PropertyTypeSearchList.as_view(), name='search-property-type'),
    path('add-street-type/', views.StreetTypeViews.as_view(), name='add-property-type'),
    path('update-street-type/', views.StreetTypeViews.as_view(), name='update-property-type'),
    path('delete-street-type/', views.StreetTypeViews.as_view(), name='delete-property-type'),
    path('search-street-type', views.StreetTypeSearchList.as_view(), name='search-property-type'),
    path('add-property/', views.PropertyView.as_view(), name='add-property'),
    path('property-details', views.PropertyView.as_view(), name='property-details'),
    path('search-property', views.PropertySearchList.as_view(), name='search-property'),
    # path('delete-property/', views.delete_property, name='delete-property'),  #Later
    path('update-property/', views.PropertyView.as_view(), name='update-property'),
]
