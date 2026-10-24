import pytest

from apps.project.models import Project

from ...models import Feature
from ...selectors import feature_list


@pytest.mark.django_db
def test_feature_list_returns_project_features_ordered_by_key():
    project = Project.objects.create(name="Project", code="feature-list")
    other_project = Project.objects.create(name="Other", code="other-project")
    second = Feature.objects.create(
        key="feature-list-2", title="Second", project=project
    )
    first = Feature.objects.create(
        key="feature-list-1", title="First", project=project
    )
    Feature.objects.create(
        key="other-project-feature", title="Other", project=other_project
    )
    Feature.objects.create(
        key="feature-list-deleted",
        title="Deleted",
        project=project,
        is_deleted=True,
    )

    results = feature_list(project_id=str(project.id))

    assert [item.id for item in results] == [str(first.id), str(second.id)]
    assert [item.title for item in results] == ["First", "Second"]
    assert all(item.project_id == str(project.id) for item in results)
