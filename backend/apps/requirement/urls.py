from django.urls import path

from .views import (
    RequirementCollectionApi,
    RequirementDetailApi,
)


app_name = "requirement"

urlpatterns = [
    path("", RequirementCollectionApi.as_view(), name="requirement-collection"),
    path(
        "<uuid:requirement_id>/",
        RequirementDetailApi.as_view(),
        name="requirement-detail",
    ),
]
