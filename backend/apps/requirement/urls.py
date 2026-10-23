from django.urls import path

from .views import (
    RequirementCollectionApi,
    RequirementVersionCollectionApi,
    RequirementVersionDetailApi,
)


app_name = "requirement"

urlpatterns = [
    path("", RequirementCollectionApi.as_view(), name="requirement-collection"),
    path(
        "<uuid:requirement_id>/versions/",
        RequirementVersionCollectionApi.as_view(),
        name="requirement-version-collection",
    ),
    path(
        "<uuid:requirement_id>/versions/<uuid:version_id>/",
        RequirementVersionDetailApi.as_view(),
        name="requirement-version-detail",
    ),
]
