from django.urls import path

from .views import ProjectCreateApi, ProjectDeleteApi


app_name = "project"

urlpatterns = [
    path("", ProjectCreateApi.as_view(), name="project-create"),
    path("<uuid:project_id>/", ProjectDeleteApi.as_view(), name="project-delete"),
]
