from django.contrib.auth import get_user_model
from django.db import transaction

from ..dtos import (
    ProjectCreateOutputDTO,
    ProjectMembershipDTO,
    ProjectMembershipCreateOutputDTO,
    ProjectUpdateOutputDTO,
)
from ..exceptions import (
    ProjectDeletionForbiddenError,
    ProjectNameRequiredError,
    ProjectMembershipAlreadyExistsError,
    ProjectMembershipManagementForbiddenError,
    ProjectMembershipOwnerRoleForbiddenError,
    ProjectNotFoundError,
    ProjectUpdateForbiddenError,
    UserNotFoundError,
)
from ..models import Project, ProjectMembership


@transaction.atomic
def project_create(*, name: str, owner_user_id: str) -> ProjectCreateOutputDTO:
    """Create a project and assign its creator the Owner role.

    Args:
        name: Display name of the project.
        owner_user_id: Identifier of the user creating the project.

    Returns:
        Serialized project data, including the owner's membership.

    Raises:
        ProjectNameRequiredError: If the name is empty after trimming.
        UserNotFoundError: If the owner user does not exist.
    """

    normalized_name = name.strip()
    if not normalized_name:
        raise ProjectNameRequiredError("Project name cannot be empty.")

    user_model = get_user_model()
    try:
        owner = user_model.objects.get(pk=owner_user_id)
    except user_model.DoesNotExist as exc:
        raise UserNotFoundError("User does not exist.") from exc

    project = Project(name=normalized_name)
    project.full_clean()
    project.save()

    membership = ProjectMembership.objects.create(
        user=owner,
        project=project,
        role=ProjectMembership.Role.OWNER,
    )

    return ProjectCreateOutputDTO(
        id=str(project.id),
        name=project.name,
        owner_membership=ProjectMembershipDTO(
            id=str(membership.id),
            user_id=str(owner.pk),
            project_id=str(project.id),
            role=membership.role,
        ),
    )


@transaction.atomic
def project_delete(*, project_id: str, user_id: str) -> None:
    """Delete a project when the requesting user is its owner.

    Args:
        project_id: Identifier of the project to delete.
        user_id: Identifier of the user requesting deletion.

    Raises:
        ProjectNotFoundError: If the project does not exist.
        ProjectDeletionForbiddenError: If the user is not the project owner.
    """

    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist as exc:
        raise ProjectNotFoundError("Project does not exist.") from exc

    is_owner = ProjectMembership.objects.filter(
        project=project,
        user_id=user_id,
        role=ProjectMembership.Role.OWNER,
    ).exists()
    if not is_owner:
        raise ProjectDeletionForbiddenError(
            "Only the project owner can delete the project."
        )

    project.delete()


@transaction.atomic
def project_update(
    *, project_id: str, user_id: str, name: str
) -> ProjectUpdateOutputDTO:
    """Update a project's name when requested by its owner.

    Args:
        project_id: Identifier of the project to update.
        user_id: Identifier of the user requesting the update.
        name: New display name of the project.

    Returns:
        Serialized project data after the update.

    Raises:
        ProjectNameRequiredError: If the name is empty after trimming.
        ProjectNotFoundError: If the project does not exist.
        ProjectUpdateForbiddenError: If the user is not the project owner.
    """

    normalized_name = name.strip()
    if not normalized_name:
        raise ProjectNameRequiredError("Project name cannot be empty.")

    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist as exc:
        raise ProjectNotFoundError("Project does not exist.") from exc

    is_owner = ProjectMembership.objects.filter(
        project=project,
        user_id=user_id,
        role=ProjectMembership.Role.OWNER,
    ).exists()
    if not is_owner:
        raise ProjectUpdateForbiddenError(
            "Only the project owner can update the project."
        )

    project.name = normalized_name
    project.full_clean()
    project.save(update_fields=["name", "updated_at"])

    return ProjectUpdateOutputDTO(id=str(project.id), name=project.name)


@transaction.atomic
def project_membership_create(
    *, project_id: str, user_id: str, requester_user_id: str, role: str
) -> ProjectMembershipCreateOutputDTO:
    """Add a user to a project with an allowed non-owner role.

    Args:
        project_id: Identifier of the project receiving the membership.
        user_id: Identifier of the user being added.
        requester_user_id: Identifier of the user managing memberships.
        role: Role assigned to the new member.

    Returns:
        Serialized membership data for the newly added member.

    Raises:
        ProjectNotFoundError: If the project does not exist.
        UserNotFoundError: If the target user does not exist.
        ProjectMembershipManagementForbiddenError: If the requester is not an owner or moderator.
        ProjectMembershipOwnerRoleForbiddenError: If the requested role is Owner or invalid.
        ProjectMembershipAlreadyExistsError: If the user is already a member.
    """

    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist as exc:
        raise ProjectNotFoundError("Project does not exist.") from exc

    requester_can_manage = ProjectMembership.objects.filter(
        project=project,
        user_id=requester_user_id,
        role__in=[
            ProjectMembership.Role.OWNER,
            ProjectMembership.Role.MODERATOR,
        ],
    ).exists()
    if not requester_can_manage:
        raise ProjectMembershipManagementForbiddenError(
            "Only project owners and moderators can manage memberships."
        )

    if role == ProjectMembership.Role.OWNER:
        raise ProjectMembershipOwnerRoleForbiddenError(
            "The Owner role cannot be assigned through membership creation."
        )

    if role not in ProjectMembership.Role.values:
        raise ProjectMembershipOwnerRoleForbiddenError(
            "The requested project membership role is invalid."
        )

    user_model = get_user_model()
    try:
        user = user_model.objects.get(pk=user_id)
    except user_model.DoesNotExist as exc:
        raise UserNotFoundError("User does not exist.") from exc

    if ProjectMembership.objects.filter(project=project, user=user).exists():
        raise ProjectMembershipAlreadyExistsError(
            "User is already a member of this project."
        )

    membership = ProjectMembership.objects.create(
        project=project,
        user=user,
        role=role,
    )

    return ProjectMembershipCreateOutputDTO(
        id=str(membership.id),
        user_id=str(user.pk),
        project_id=str(project.id),
        role=membership.role,
    )
