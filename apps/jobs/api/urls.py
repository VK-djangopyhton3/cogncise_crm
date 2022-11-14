from django.urls import path

from apps.jobs.api import views

urlpatterns = [
    path('add-work-type/', views.create_work_type, name='add-property-type'),
    path('update-work-type/', views.update_work_type, name='update-property-type'),
    path('delete-work-type/', views.delete_work_type, name='delete-property-type'),
    path('search-work-type', views.WorkTypeSearchList.as_view(), name='search-property-type'),
    path('add-job/', views.add_job, name='add-job')
]
