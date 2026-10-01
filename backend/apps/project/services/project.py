from django.contrib.auth import get_user_model
from django.db import transaction

from apps.project.dtos import ProjectCreateOutputDTO, ProjectMembershipDTO
from apps.project.exceptions import (
    ProjectNameRequiredError,
    UserNotFoundError,
)
from apps.project.models import Project, ProjectMembership


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
