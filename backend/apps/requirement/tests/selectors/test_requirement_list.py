import pytest
from django.contrib.auth import get_user_model

from apps.project.models import Project

from ...models import Feature, Requirement
from ...selectors import requirement_list


@pytest.mark.django_db
def test_requirement_list_returns_all_non_deleted_project_requirements():
    user = get_user_model().objects.create_user(username="requirement-list-user")
    project = Project.objects.create(name="Project", code="requirement-list")
    feature = Feature.objects.create(
        key="requirement-list-feature", title="Feature", project=project
    )
    first = Requirement.objects.create(
        key="requirement-list-1",
        created_by=user,
        title="First",
        description="First requirement",
        feature=feature,
    )
    second = Requirement.objects.create(
        key="requirement-list-2",
        created_by=user,
        title="Second",
        description="Second requirement",
        feature=feature,
    )
    Requirement.objects.create(
        key="requirement-list-deleted",
        created_by=user,
        title="Deleted",
        description="Deleted requirement",
        feature=feature,
        is_deleted=True,
    )

    results = requirement_list(project_id=str(project.id))

    assert [item.id for item in results] == [str(first.id), str(second.id)]
    assert [item.title for item in results] == ["First", "Second"]
