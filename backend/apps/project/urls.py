from django.urls import path

from .views import ProjectCollectionApi, ProjectDetailApi


app_name = "project"

urlpatterns = [
    path("", ProjectCollectionApi.as_view(), name="project-collection"),
    path("<uuid:project_id>/", ProjectDetailApi.as_view(), name="project-detail"),
]
