import uuid

import pytest
from django.contrib.auth import get_user_model

from ...exceptions import (
    ProjectDeletionForbiddenError,
    ProjectNotFoundError,
)
from ...models import Project, ProjectMembership
from ...services import project_delete


@pytest.mark.django_db
def test_project_delete_owner_soft_deletes_project_and_preserves_memberships():
    # Arrange
    owner = get_user_model().objects.create_user(username="project-owner")
    project = Project.objects.create(name="Requirements Tool", code="requirements-tool")
    ProjectMembership.objects.create(
        user=owner,
        project=project,
        role=ProjectMembership.Role.OWNER,
    )

    # Act
    project_delete(project_id=str(project.id), user_id=str(owner.pk))

    # Assert
    project.refresh_from_db()
    assert project.is_deleted is True
    assert Project.objects.filter(id=project.id).exists()
    assert ProjectMembership.objects.filter(project_id=project.id).exists()


@pytest.mark.django_db
def test_project_delete_non_owner_is_forbidden():
    # Arrange
    owner = get_user_model().objects.create_user(username="project-owner")
    member = get_user_model().objects.create_user(username="project-member")
    project = Project.objects.create(name="Requirements Tool", code="requirements-tool")
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
    with pytest.raises(ProjectDeletionForbiddenError):
        project_delete(project_id=str(project.id), user_id=str(member.pk))

    # Assert
    assert Project.objects.filter(id=project.id).exists()


@pytest.mark.django_db
def test_project_delete_project_does_not_exist():
    # Arrange
    project_id = str(uuid.uuid4())
    user_id = "999999"

    # Act
    with pytest.raises(ProjectNotFoundError):
        project_delete(project_id=project_id, user_id=user_id)

    # Assert
    assert Project.objects.count() == 0
