from django.urls import path

from .views import (
    BusinessRuleCollectionApi,
    BusinessRuleDetailApi,
    FeatureCollectionApi,
    FeatureDetailApi,
    RequirementCollectionApi,
    RequirementDetailApi,
    ReleaseVersionCollectionApi,
    ReleaseVersionDetailApi,
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
    path(
        "business-rules/",
        BusinessRuleCollectionApi.as_view(),
        name="business-rule-collection",
    ),
    path(
        "business-rules/<uuid:business_rule_id>/",
        BusinessRuleDetailApi.as_view(),
        name="business-rule-detail",
    ),
    path(
        "release-versions/",
        ReleaseVersionCollectionApi.as_view(),
        name="release-version-collection",
    ),
    path(
        "release-versions/<uuid:release_version_id>/",
        ReleaseVersionDetailApi.as_view(),
        name="release-version-detail",
    ),
]
