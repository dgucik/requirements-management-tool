from django.urls import path

from .views import RequirementCollectionApi


app_name = "requirement"

urlpatterns = [
    path("", RequirementCollectionApi.as_view(), name="requirement-collection"),
]
