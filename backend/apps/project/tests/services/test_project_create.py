import pytest
from django.contrib.auth import get_user_model

from apps.project.exceptions import ProjectNameRequiredError, UserNotFoundError
from apps.project.models import Project, ProjectMembership
from apps.project.services import project_create


@pytest.mark.django_db
def test_project_create_happy_path():
    # Arrange
    user = get_user_model().objects.create_user(
        username="project-owner",
        password="test-password",
    )

    # Act
    result = project_create(name="Requirements Tool", owner_user_id=str(user.pk))

    # Assert
    project = Project.objects.get(id=result.id)
    membership = ProjectMembership.objects.get(project=project, user=user)

    assert project.name == "Requirements Tool"
    assert membership.role == ProjectMembership.Role.OWNER
    assert result.owner_membership.role == ProjectMembership.Role.OWNER


@pytest.mark.django_db
def test_project_create_user_does_not_exist():
    # Arrange
    user_id = "999999"

    # Act
    with pytest.raises(UserNotFoundError):
        project_create(name="Requirements Tool", owner_user_id=user_id)

    # Assert
    assert Project.objects.count() == 0
    assert ProjectMembership.objects.count() == 0


@pytest.mark.django_db
def test_project_create_name_is_empty():
    # Arrange
    user = get_user_model().objects.create_user(
        username="project-owner",
        password="test-password",
    )

    # Act
    with pytest.raises(ProjectNameRequiredError):
        project_create(name="   ", owner_user_id=str(user.pk))

    # Assert
    assert Project.objects.count() == 0
    assert ProjectMembership.objects.count() == 0
