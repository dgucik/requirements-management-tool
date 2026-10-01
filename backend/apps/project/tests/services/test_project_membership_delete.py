import pytest
from django.contrib.auth import get_user_model

from ...exceptions import ProjectOwnerMembershipDeletionForbiddenError
from ...models import Project, ProjectMembership
from ...services import project_membership_delete


@pytest.mark.django_db
def test_project_membership_delete_owner_deletes_member():
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
        role=ProjectMembership.Role.EDITOR,
    )

    # Act
    project_membership_delete(
        project_id=str(project.id),
        membership_id=str(membership.id),
        requester_user_id=str(owner.pk),
    )

    # Assert
    assert not ProjectMembership.objects.filter(id=membership.id).exists()


@pytest.mark.django_db
def test_project_membership_delete_moderator_deletes_member():
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
    project_membership_delete(
        project_id=str(project.id),
        membership_id=str(membership.id),
        requester_user_id=str(moderator.pk),
    )

    # Assert
    assert not ProjectMembership.objects.filter(id=membership.id).exists()


@pytest.mark.django_db
def test_project_membership_delete_moderator_cannot_delete_owner():
    # Arrange
    user_model = get_user_model()
    moderator = user_model.objects.create_user(username="project-moderator")
    owner = user_model.objects.create_user(username="project-owner")
    project = Project.objects.create(name="Requirements Tool")
    ProjectMembership.objects.create(
        user=moderator,
        project=project,
        role=ProjectMembership.Role.MODERATOR,
    )
    owner_membership = ProjectMembership.objects.create(
        user=owner,
        project=project,
        role=ProjectMembership.Role.OWNER,
    )

    # Act
    with pytest.raises(ProjectOwnerMembershipDeletionForbiddenError):
        project_membership_delete(
            project_id=str(project.id),
            membership_id=str(owner_membership.id),
            requester_user_id=str(moderator.pk),
        )

    # Assert
    assert ProjectMembership.objects.filter(id=owner_membership.id).exists()
