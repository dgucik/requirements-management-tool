import pytest
from django.contrib.auth import get_user_model

from apps.project.exceptions import (
    ProjectNameRequiredError,
    ProjectUpdateForbiddenError,
)
from apps.project.models import Project, ProjectMembership
from apps.project.services import project_update


@pytest.mark.django_db
def test_project_update_owner_changes_name():
    # Arrange
    owner = get_user_model().objects.create_user(username="project-owner")
    project = Project.objects.create(name="Old name")
    ProjectMembership.objects.create(
        user=owner,
        project=project,
        role=ProjectMembership.Role.OWNER,
    )

    # Act
    result = project_update(
        project_id=str(project.id),
        user_id=str(owner.pk),
        name="New name",
    )

    # Assert
    project.refresh_from_db()
    assert project.name == "New name"
    assert result.id == str(project.id)
    assert result.name == "New name"


@pytest.mark.django_db
def test_project_update_non_owner_is_forbidden():
    # Arrange
    owner = get_user_model().objects.create_user(username="project-owner")
    member = get_user_model().objects.create_user(username="project-member")
    project = Project.objects.create(name="Old name")
    ProjectMembership.objects.create(
        user=owner,
        project=project,
        role=ProjectMembership.Role.OWNER,
    )
    ProjectMembership.objects.create(
        user=member,
        project=project,
        role=ProjectMembership.Role.EDITOR,
    )

    # Act
    with pytest.raises(ProjectUpdateForbiddenError):
        project_update(
            project_id=str(project.id),
            user_id=str(member.pk),
            name="New name",
        )

    # Assert
    project.refresh_from_db()
    assert project.name == "Old name"


@pytest.mark.django_db
def test_project_update_name_is_empty():
    # Arrange
    owner = get_user_model().objects.create_user(username="project-owner")
    project = Project.objects.create(name="Old name")
    ProjectMembership.objects.create(
        user=owner,
        project=project,
        role=ProjectMembership.Role.OWNER,
    )

    # Act
    with pytest.raises(ProjectNameRequiredError):
        project_update(
            project_id=str(project.id),
            user_id=str(owner.pk),
            name="   ",
        )

    # Assert
    project.refresh_from_db()
    assert project.name == "Old name"
