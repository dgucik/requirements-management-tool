from django.contrib.auth import get_user_model
from django.db import transaction

from ..dtos import ProjectCreateDTO, ProjectCreateMembershipDTO, ProjectUpdateDTO
from ..exceptions import (
    ProjectDeletionForbiddenError,
    ProjectNameRequiredError,
    ProjectNotFoundError,
    ProjectUpdateForbiddenError,
    UserNotFoundError,
)
from ..models import Project, ProjectMembership


@transaction.atomic
def project_create(*, name: str, owner_user_id: str) -> ProjectCreateDTO:
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

    return ProjectCreateDTO(
        id=str(project.id),
        name=project.name,
        owner_membership=ProjectCreateMembershipDTO(
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
) -> ProjectUpdateDTO:
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

    return ProjectUpdateDTO(id=str(project.id), name=project.name)
