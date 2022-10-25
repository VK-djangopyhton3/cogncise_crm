from django.urls import path

from apps.users.api import views

urlpatterns = [
    path('staff/add-user/', views.UserCreateOrDeleteView.as_view(), name="create-user"),
    path('/update-info/', views..as_view(), name="create-user")
]
