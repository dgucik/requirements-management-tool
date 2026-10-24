import pytest

from apps.project.models import Project

from ...models import ReleaseVersion
from ...selectors import release_version_list


@pytest.mark.django_db
def test_release_version_list_returns_versions_ordered_by_name():
    project = Project.objects.create(name="Project", code="release-list")
    other_project = Project.objects.create(name="Other", code="release-other")
    second = ReleaseVersion.objects.create(name="2.0", project=project)
    first = ReleaseVersion.objects.create(name="1.0", project=project)
    ReleaseVersion.objects.create(name="0.1", project=other_project)

    results = release_version_list(project_id=str(project.id))

    assert [result.id for result in results] == [str(first.id), str(second.id)]
    assert [result.name for result in results] == ["1.0", "2.0"]
    assert all(result.project_id == str(project.id) for result in results)
