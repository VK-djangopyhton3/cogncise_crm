from django.urls import path

from apps.users.api import views

urlpatterns = [
    path('add-user/', views.UserViews.as_view(), name="create-user"),
    path('update-user/', views.UserViews.as_view(), name="update-user"),
    path('delete-user', views.UserViews.as_view(), name="delete-user"),
    path('list-users', views.UserSearchList.as_view(), name="list-user"),
    path('view-user', views.UserViews.as_view(), name="view-user"),
    path('assign-role/', views.UserRolesViews.as_view(), name="assign-role"),
    path('update-role/', views.UserRolesViews.as_view(), name="update-role"),
    path('staff/associate-staff/', views.assign_companies, name="associate-staff"),
]
