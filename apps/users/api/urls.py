from django.urls import path

from apps.users.api import views

urlpatterns = [
    path('staff/adduser/', views.UserViews.as_view(), name="")
]
