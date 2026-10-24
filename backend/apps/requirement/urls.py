from django.urls import path

from .views import (
    FeatureCollectionApi,
    FeatureDetailApi,
    RequirementCollectionApi,
    RequirementDetailApi,
)


app_name = "requirement"

urlpatterns = [
    path(
        "requirements/",
        RequirementCollectionApi.as_view(),
        name="requirement-collection",
    ),
    path(
        "requirements/<uuid:requirement_id>/",
        RequirementDetailApi.as_view(),
        name="requirement-detail",
    ),
    path(
        "features/",
        FeatureCollectionApi.as_view(),
        name="feature-collection",
    ),
    path(
        "features/<uuid:feature_id>/",
        FeatureDetailApi.as_view(),
        name="feature-detail",
    ),
]
