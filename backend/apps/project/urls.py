from django.urls import path

from .views import ProjectCreateApi


app_name = "project"

urlpatterns = [
    path("", ProjectCreateApi.as_view(), name="project-create"),
]
