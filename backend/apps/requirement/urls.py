from django.urls import path

from .views import RequirementCollectionApi, RequirementVersionCollectionApi


app_name = "requirement"

urlpatterns = [
    path("", RequirementCollectionApi.as_view(), name="requirement-collection"),
    path(
        "<uuid:requirement_id>/versions/",
        RequirementVersionCollectionApi.as_view(),
        name="requirement-version-collection",
    ),
]
