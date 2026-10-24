from django.urls import include, path

from .views import (
    ProjectCollectionApi,
    ProjectDetailApi,
    ProjectMembershipCollectionApi,
    ProjectMembershipDetailApi,
)


app_name = "project"

urlpatterns = [
    path("", ProjectCollectionApi.as_view(), name="project-collection"),
    path(
        "<uuid:project_id>/",
        include("apps.requirement.urls"),
    ),
    path(
        "<uuid:project_id>/memberships/",
        ProjectMembershipCollectionApi.as_view(),
        name="project-membership-collection",
    ),
    path(
        "<uuid:project_id>/memberships/<uuid:membership_id>/",
        ProjectMembershipDetailApi.as_view(),
        name="project-membership-detail",
    ),
    path("<uuid:project_id>/", ProjectDetailApi.as_view(), name="project-detail"),
]
