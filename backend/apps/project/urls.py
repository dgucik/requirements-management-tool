from django.urls import path

from .views import ProjectCreateApi, ProjectDetailApi


app_name = "project"

urlpatterns = [
    path("", ProjectCreateApi.as_view(), name="project-create"),
    path("<uuid:project_id>/", ProjectDetailApi.as_view(), name="project-detail"),
]
