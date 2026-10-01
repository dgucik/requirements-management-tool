import pytest
from django.contrib.auth import get_user_model

from ...exceptions import ProjectNotFoundError
from ...models import Project, ProjectMembership
from ...selectors import project_membership_list


@pytest.mark.django_db
def test_project_membership_list_returns_project_memberships_with_roles():
    # Arrange
    user_model = get_user_model()
    first_user = user_model.objects.create_user(username="first-member")
    second_user = user_model.objects.create_user(username="second-member")
    project = Project.objects.create(name="Requirements Tool")
    first_membership = ProjectMembership.objects.create(
        user=first_user,
        project=project,
        role=ProjectMembership.Role.OWNER,
    )
    second_membership = ProjectMembership.objects.create(
        user=second_user,
        project=project,
        role=ProjectMembership.Role.EDITOR,
    )

    # Act
    result = project_membership_list(project_id=str(project.id))

    # Assert
    assert [(membership.id, membership.role) for membership in result] == [
        (str(first_membership.id), ProjectMembership.Role.OWNER),
        (str(second_membership.id), ProjectMembership.Role.EDITOR),
    ]


@pytest.mark.django_db
def test_project_membership_list_project_does_not_exist():
    # Arrange
    project_id = "00000000-0000-0000-0000-000000000000"

    # Act
    with pytest.raises(ProjectNotFoundError):
        project_membership_list(project_id=project_id)

    # Assert
    assert Project.objects.count() == 0
