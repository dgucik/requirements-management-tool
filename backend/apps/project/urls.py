from django.urls import path

from .views import (
    ProjectCollectionApi,
    ProjectDetailApi,
    ProjectMembershipApi,
)


app_name = "project"

urlpatterns = [
    path("", ProjectCollectionApi.as_view(), name="project-collection"),
    path(
        "<uuid:project_id>/memberships/",
        ProjectMembershipApi.as_view(),
        name="project-membership-create",
    ),
    path(
        "<uuid:project_id>/memberships/<uuid:membership_id>/",
        ProjectMembershipApi.as_view(),
        name="project-membership-detail",
    ),
    path("<uuid:project_id>/", ProjectDetailApi.as_view(), name="project-detail"),
]
