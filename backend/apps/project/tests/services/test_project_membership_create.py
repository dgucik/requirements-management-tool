import pytest
from django.contrib.auth import get_user_model

from ...exceptions import (
    ProjectMembershipManagementForbiddenError,
    ProjectMembershipOwnerRoleForbiddenError,
)
from ...models import Project, ProjectMembership
from ...services import project_membership_create


@pytest.mark.django_db
def test_project_membership_create_owner_adds_member():
    # Arrange
    user_model = get_user_model()
    owner = user_model.objects.create_user(username="project-owner")
    new_member = user_model.objects.create_user(username="new-member")
    project = Project.objects.create(name="Requirements Tool")
    ProjectMembership.objects.create(
        user=owner,
        project=project,
        role=ProjectMembership.Role.OWNER,
    )

    # Act
    result = project_membership_create(
        project_id=str(project.id),
        user_id=str(new_member.pk),
        requester_user_id=str(owner.pk),
        role=ProjectMembership.Role.EDITOR,
    )

    # Assert
    membership = ProjectMembership.objects.get(id=result.id)
    assert membership.user_id == new_member.pk
    assert membership.project_id == project.id
    assert membership.role == ProjectMembership.Role.EDITOR


@pytest.mark.django_db
def test_project_membership_create_moderator_adds_member():
    # Arrange
    user_model = get_user_model()
    moderator = user_model.objects.create_user(username="project-moderator")
    new_member = user_model.objects.create_user(username="new-member")
    project = Project.objects.create(name="Requirements Tool")
    ProjectMembership.objects.create(
        user=moderator,
        project=project,
        role=ProjectMembership.Role.MODERATOR,
    )

    # Act
    result = project_membership_create(
        project_id=str(project.id),
        user_id=str(new_member.pk),
        requester_user_id=str(moderator.pk),
        role=ProjectMembership.Role.VIEWER,
    )

    # Assert
    assert result.role == ProjectMembership.Role.VIEWER
    assert ProjectMembership.objects.filter(
        project=project,
        user=new_member,
        role=ProjectMembership.Role.VIEWER,
    ).exists()


@pytest.mark.django_db
def test_project_membership_create_non_manager_is_forbidden():
    # Arrange
    user_model = get_user_model()
    member = user_model.objects.create_user(username="project-member")
    new_member = user_model.objects.create_user(username="new-member")
    project = Project.objects.create(name="Requirements Tool")
    ProjectMembership.objects.create(
        user=member,
        project=project,
        role=ProjectMembership.Role.EDITOR,
    )

    # Act
    with pytest.raises(ProjectMembershipManagementForbiddenError):
        project_membership_create(
            project_id=str(project.id),
            user_id=str(new_member.pk),
            requester_user_id=str(member.pk),
            role=ProjectMembership.Role.VIEWER,
        )

    # Assert
    assert ProjectMembership.objects.filter(project=project).count() == 1


@pytest.mark.django_db
def test_project_membership_create_owner_role_is_forbidden():
    # Arrange
    user_model = get_user_model()
    owner = user_model.objects.create_user(username="project-owner")
    new_member = user_model.objects.create_user(username="new-member")
    project = Project.objects.create(name="Requirements Tool")
    ProjectMembership.objects.create(
        user=owner,
        project=project,
        role=ProjectMembership.Role.OWNER,
    )

    # Act
    with pytest.raises(ProjectMembershipOwnerRoleForbiddenError):
        project_membership_create(
            project_id=str(project.id),
            user_id=str(new_member.pk),
            requester_user_id=str(owner.pk),
            role=ProjectMembership.Role.OWNER,
        )

    # Assert
    assert ProjectMembership.objects.filter(project=project).count() == 1
