from django.urls import path

from apps.users.api import views

urlpatterns = [
    path('staff/add-user/', views.add_user, name="create-user"),
    path('update-user/', views.update_user_details, name="update-user"),
    path('delete-user', views.delete_user, name="delete-user"),
    path('list-users', views.UserSearchList.as_view(), name="list-user"),
    path('view-users', views.view_user, name="list-user"),
    path('assign-role/', views.assign_role, name="list-user"),
]
