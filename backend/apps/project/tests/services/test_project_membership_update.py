import pytest
from django.contrib.auth import get_user_model

from ...exceptions import (
    ProjectMembershipManagementForbiddenError,
    ProjectMembershipOwnerRoleForbiddenError,
)
from ...models import Project, ProjectMembership
from ...services import project_membership_update


@pytest.mark.django_db
def test_project_membership_update_owner_updates_role():
    # Arrange
    user_model = get_user_model()
    owner = user_model.objects.create_user(username="project-owner")
    member = user_model.objects.create_user(username="project-member")
    project = Project.objects.create(name="Requirements Tool")
    ProjectMembership.objects.create(
        user=owner,
        project=project,
        role=ProjectMembership.Role.OWNER,
    )
    membership = ProjectMembership.objects.create(
        user=member,
        project=project,
        role=ProjectMembership.Role.VIEWER,
    )

    # Act
    result = project_membership_update(
        project_id=str(project.id),
        membership_id=str(membership.id),
        requester_user_id=str(owner.pk),
        role=ProjectMembership.Role.EDITOR,
    )

    # Assert
    assert result.role == ProjectMembership.Role.EDITOR
    membership.refresh_from_db()
    assert membership.role == ProjectMembership.Role.EDITOR


@pytest.mark.django_db
def test_project_membership_update_moderator_updates_role():
    # Arrange
    user_model = get_user_model()
    moderator = user_model.objects.create_user(username="project-moderator")
    member = user_model.objects.create_user(username="project-member")
    project = Project.objects.create(name="Requirements Tool")
    ProjectMembership.objects.create(
        user=moderator,
        project=project,
        role=ProjectMembership.Role.MODERATOR,
    )
    membership = ProjectMembership.objects.create(
        user=member,
        project=project,
        role=ProjectMembership.Role.VIEWER,
    )

    # Act
    project_membership_update(
        project_id=str(project.id),
        membership_id=str(membership.id),
        requester_user_id=str(moderator.pk),
        role=ProjectMembership.Role.EDITOR,
    )

    # Assert
    membership.refresh_from_db()
    assert membership.role == ProjectMembership.Role.EDITOR


@pytest.mark.django_db
def test_project_membership_update_non_manager_is_forbidden():
    # Arrange
    user_model = get_user_model()
    member = user_model.objects.create_user(username="project-member")
    target = user_model.objects.create_user(username="target-member")
    project = Project.objects.create(name="Requirements Tool")
    ProjectMembership.objects.create(
        user=member,
        project=project,
        role=ProjectMembership.Role.EDITOR,
    )
    membership = ProjectMembership.objects.create(
        user=target,
        project=project,
        role=ProjectMembership.Role.VIEWER,
    )

    # Act
    with pytest.raises(ProjectMembershipManagementForbiddenError):
        project_membership_update(
            project_id=str(project.id),
            membership_id=str(membership.id),
            requester_user_id=str(member.pk),
            role=ProjectMembership.Role.MODERATOR,
        )

    # Assert
    membership.refresh_from_db()
    assert membership.role == ProjectMembership.Role.VIEWER


@pytest.mark.django_db
def test_project_membership_update_owner_role_is_forbidden():
    # Arrange
    user_model = get_user_model()
    owner = user_model.objects.create_user(username="project-owner")
    member = user_model.objects.create_user(username="project-member")
    project = Project.objects.create(name="Requirements Tool")
    ProjectMembership.objects.create(
        user=owner,
        project=project,
        role=ProjectMembership.Role.OWNER,
    )
    membership = ProjectMembership.objects.create(
        user=member,
        project=project,
        role=ProjectMembership.Role.VIEWER,
    )

    # Act
    with pytest.raises(ProjectMembershipOwnerRoleForbiddenError):
        project_membership_update(
            project_id=str(project.id),
            membership_id=str(membership.id),
            requester_user_id=str(owner.pk),
            role=ProjectMembership.Role.OWNER,
        )

    # Assert
    membership.refresh_from_db()
    assert membership.role == ProjectMembership.Role.VIEWER
