import pytest

from apps.project.models import Project

from ...models import BusinessRule, Feature, Requirement
from ...selectors import key_existing_list


@pytest.mark.django_db
def test_key_existing_list_returns_keys_from_all_supported_items():
    project = Project.objects.create(name="Requirements Tool", code="project")
    feature = Feature.objects.create(
        key="project-1",
        title="Login",
        project=project,
    )
    BusinessRule.objects.create(key="project-2", rule="A valid session is required.")
    Requirement.objects.create(key="project-3")

    assert key_existing_list() == ["project-1", "project-2", "project-3"]
