import pytest
from django.contrib.auth import get_user_model

from apps.project.models import Project, ProjectMembership

from ...models import ReleaseVersion, Requirement
from ...services import (
    release_version_create,
    release_version_delete,
    release_version_update,
)


@pytest.fixture
def release_version_context():
    user = get_user_model().objects.create_user(username="release-version-user")
    project = Project.objects.create(name="Project", code="release-version")
    ProjectMembership.objects.create(
        user=user,
        project=project,
        role=ProjectMembership.Role.EDITOR,
    )
    return user, project


@pytest.mark.django_db
def test_release_version_create_normalizes_name(release_version_context):
    user, project = release_version_context

    result = release_version_create(
        project_id=str(project.id),
        user_id=str(user.id),
        name="  Release 1  ",
    )

    assert result.name == "Release 1"
    assert ReleaseVersion.objects.filter(pk=result.id, name="Release 1").exists()


@pytest.mark.django_db
def test_release_version_update_changes_name(release_version_context):
    user, project = release_version_context
    release_version = ReleaseVersion.objects.create(
        name="Old release",
        project=project,
    )

    result = release_version_update(
        project_id=str(project.id),
        release_version_id=str(release_version.id),
        user_id=str(user.id),
        name=" New release ",
    )

    release_version.refresh_from_db()
    assert result.name == "New release"
    assert release_version.name == "New release"


@pytest.mark.django_db
def test_release_version_delete_removes_row_and_nulls_requirement_reference(
    release_version_context,
):
    user, project = release_version_context
    release_version = ReleaseVersion.objects.create(
        name="Delete release",
        project=project,
    )
    requirement = Requirement.objects.create(
        key="release-version-requirement",
        title="Requirement",
        description="Description",
        target_release_version=release_version,
    )

    result = release_version_delete(
        project_id=str(project.id),
        release_version_id=str(release_version.id),
        user_id=str(user.id),
    )

    requirement.refresh_from_db()
    assert result.id == str(release_version.id)
    assert not ReleaseVersion.objects.filter(pk=release_version.id).exists()
    assert requirement.target_release_version_id is None
