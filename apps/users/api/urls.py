from django.urls import path

from apps.users.api import views

urlpatterns = [
    path('staff/adduser/', views.UserCreateView.as_view(), name="create-user")
]
