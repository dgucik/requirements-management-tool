from django.urls import path

from .views import (
    ProjectCollectionApi,
    ProjectDetailApi,
    ProjectMembershipCreateApi,
)


app_name = "project"

urlpatterns = [
    path("", ProjectCollectionApi.as_view(), name="project-collection"),
    path(
        "<uuid:project_id>/memberships/",
        ProjectMembershipCreateApi.as_view(),
        name="project-membership-create",
    ),
    path("<uuid:project_id>/", ProjectDetailApi.as_view(), name="project-detail"),
]
