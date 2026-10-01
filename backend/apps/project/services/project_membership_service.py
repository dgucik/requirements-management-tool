from django.contrib.auth import get_user_model
from django.db import transaction

from ..dtos import ProjectMembershipCreateDTO
from ..exceptions import (
    ProjectMembershipAlreadyExistsError,
    ProjectMembershipManagementForbiddenError,
    ProjectMembershipOwnerRoleForbiddenError,
    ProjectNotFoundError,
    UserNotFoundError,
)
from ..models import Project, ProjectMembership


@transaction.atomic
def project_membership_create(
    *, project_id: str, user_id: str, requester_user_id: str, role: str
) -> ProjectMembershipCreateDTO:
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

    return ProjectMembershipCreateDTO(
        id=str(membership.id),
        user_id=str(user.pk),
        project_id=str(project.id),
        role=membership.role,
    )
