from django.urls import path

from apps.jobs.api import views

urlpatterns = [
    path("add-work-type/", views.WorkTypeView.as_view(), name="add-work-type"),
    path("update-work-type/", views.WorkTypeView.as_view(), name="update-work-type"),
    path("search-work-type", views.WorkTypeSearch.as_view(), name="search-work-type"),
    path("delete-work-type/", views.WorkTypeView.as_view(), name="delete-work-type"),
    path("add-job/", views.JobsViews.as_view(), name="add-job"),
    path("update-job/", views.JobsViews.as_view(), name="update-job"),
    path("get-job", views.JobsViews.as_view(), name="get-job"),
    path("search-job", views.JobSearchList.as_view(), name="search-job"),

]
