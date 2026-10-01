import uuid

import pytest
from django.contrib.auth import get_user_model

from apps.project.exceptions import (
    ProjectDeletionForbiddenError,
    ProjectNotFoundError,
)
from apps.project.models import Project, ProjectMembership
from apps.project.services import project_delete


@pytest.mark.django_db
def test_project_delete_owner_deletes_project_and_memberships():
    # Arrange
    owner = get_user_model().objects.create_user(username="project-owner")
    project = Project.objects.create(name="Requirements Tool")
    ProjectMembership.objects.create(
        user=owner,
        project=project,
        role=ProjectMembership.Role.OWNER,
    )

    # Act
    project_delete(project_id=str(project.id), user_id=str(owner.pk))

    # Assert
    assert not Project.objects.filter(id=project.id).exists()
    assert not ProjectMembership.objects.filter(project_id=project.id).exists()


@pytest.mark.django_db
def test_project_delete_non_owner_is_forbidden():
    # Arrange
    owner = get_user_model().objects.create_user(username="project-owner")
    member = get_user_model().objects.create_user(username="project-member")
    project = Project.objects.create(name="Requirements Tool")
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
