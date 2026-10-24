from django.db import transaction

from apps.project.selectors import project_get, project_user_has_edit_permissions

from ..dtos import (
    ReleaseVersionCreateDTO,
    ReleaseVersionDeleteDTO,
    ReleaseVersionUpdateDTO,
)
from ..exceptions import (
    ReleaseVersionCreationForbiddenError,
    ReleaseVersionDeleteForbiddenError,
    ReleaseVersionNameAlreadyExistsError,
    ReleaseVersionNameRequiredError,
    ReleaseVersionNotFoundError,
    ReleaseVersionUpdateForbiddenError,
)
from ..models import ReleaseVersion


def _normalized_name(name: str) -> str:
    """Return a validated release version name."""

    normalized_name = name.strip()
    if not normalized_name:
        raise ReleaseVersionNameRequiredError(
            "Release version name cannot be empty."
        )
    return normalized_name


@transaction.atomic
def release_version_create(
    *, project_id: str, user_id: str, name: str
) -> ReleaseVersionCreateDTO:
    """Create a release version.

    Args:
        project_id: Identifier of the project whose release catalog is managed.
        user_id: Identifier of the user creating the release version.
        name: Release version name.

    Returns:
        Serialized created release version.
    """

    project_get(project_id=project_id)
    if not project_user_has_edit_permissions(project_id=project_id, user_id=user_id):
        raise ReleaseVersionCreationForbiddenError(
            "Only project editors, moderators, and owners can create release versions."
        )
    normalized_name = _normalized_name(name)
    if ReleaseVersion.objects.filter(name=normalized_name).exists():
        raise ReleaseVersionNameAlreadyExistsError(
            "A release version with this name already exists."
        )

    release_version = ReleaseVersion.objects.create(
        name=normalized_name,
        project_id=project_id,
    )
    return ReleaseVersionCreateDTO(
        id=str(release_version.id),
        name=release_version.name,
        project_id=str(project_id),
    )


@transaction.atomic
def release_version_update(
    *, project_id: str, release_version_id: str, user_id: str, name: str
) -> ReleaseVersionUpdateDTO:
    """Update a release version name.

    Args:
        project_id: Identifier of the project whose release catalog is managed.
        release_version_id: Identifier of the release version to update.
        user_id: Identifier of the user requesting the update.
        name: New release version name.

    Returns:
        Serialized updated release version.
    """

    if not project_user_has_edit_permissions(project_id=project_id, user_id=user_id):
        raise ReleaseVersionUpdateForbiddenError(
            "Only project editors, moderators, and owners can update release versions."
        )
    normalized_name = _normalized_name(name)
    release_version = (
        ReleaseVersion.objects.select_for_update()
        .filter(pk=release_version_id, project_id=project_id)
        .first()
    )
    if release_version is None:
        raise ReleaseVersionNotFoundError("Release version does not exist.")
    if ReleaseVersion.objects.filter(name=normalized_name).exclude(
        pk=release_version.id
    ).exists():
        raise ReleaseVersionNameAlreadyExistsError(
            "A release version with this name already exists."
        )

    release_version.name = normalized_name
    release_version.save(update_fields=["name", "updated_at"])
    return ReleaseVersionUpdateDTO(
        id=str(release_version.id),
        name=release_version.name,
        project_id=str(release_version.project_id),
    )


@transaction.atomic
def release_version_delete(
    *, project_id: str, release_version_id: str, user_id: str
) -> ReleaseVersionDeleteDTO:
    """Permanently delete a release version.

    Args:
        project_id: Identifier of the project whose release catalog is managed.
        release_version_id: Identifier of the release version to delete.
        user_id: Identifier of the user requesting deletion.

    Returns:
        Serialized deletion result.
    """

    if not project_user_has_edit_permissions(project_id=project_id, user_id=user_id):
        raise ReleaseVersionDeleteForbiddenError(
            "Only project editors, moderators, and owners can delete release versions."
        )
    release_version = (
        ReleaseVersion.objects.select_for_update()
        .filter(pk=release_version_id, project_id=project_id)
        .first()
    )
    if release_version is None:
        raise ReleaseVersionNotFoundError("Release version does not exist.")

    release_version_id = str(release_version.id)
    release_version.delete()
    return ReleaseVersionDeleteDTO(id=release_version_id)
