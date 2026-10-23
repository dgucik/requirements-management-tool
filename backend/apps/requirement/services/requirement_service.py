from django.db import transaction

from apps.project.models import Project
from apps.project.selectors import project_user_has_edit_permissions

from ..dtos import RequirementCreateDTO, RequirementDeleteDTO, RequirementUpdateDTO
from ..exceptions import (
    RequirementCreationForbiddenError,
    RequirementDeleteForbiddenError,
    RequirementDescriptionRequiredError,
    RequirementFeatureNotFoundError,
    RequirementNotFoundError,
    RequirementReleaseVersionNotFoundError,
    RequirementTitleRequiredError,
    RequirementUpdateForbiddenError,
)
from ..identifiers import requirement_key_generate
from ..models import Feature, ReleaseVersion, Requirement
from ..selectors import key_existing_list


def requirement_create(
    *,
    project_id: str,
    user_id: str,
    title: str,
    description: str,
    feature_id: str,
) -> RequirementCreateDTO:
    """Create a requirement in a project.

    Args:
        project_id: Identifier of the project receiving the requirement.
        user_id: Identifier of the user creating the requirement.
        title: Requirement title.
        description: Requirement description.
        feature_id: Identifier of the feature assigned to the requirement.

    Returns:
        Serialized data for the created requirement.
    """

    if not project_user_has_edit_permissions(project_id=project_id, user_id=user_id):
        raise RequirementCreationForbiddenError(
            "Only project editors, moderators, and owners can create requirements."
        )

    normalized_title = title.strip()
    if not normalized_title:
        raise RequirementTitleRequiredError("Requirement title cannot be empty.")
    normalized_description = description.strip()
    if not normalized_description:
        raise RequirementDescriptionRequiredError(
            "Requirement description cannot be empty."
        )

    project = Project.objects.get(pk=project_id)
    try:
        feature = Feature.objects.get(pk=feature_id, project_id=project.id)
    except Feature.DoesNotExist as exc:
        raise RequirementFeatureNotFoundError(
            "Feature does not exist in the selected project."
        ) from exc

    requirement = Requirement.objects.create(
        key=requirement_key_generate(
            project_code=project.code,
            existing_keys=key_existing_list(),
        ),
        created_by_id=user_id,
        title=normalized_title,
        description=normalized_description,
        feature=feature,
    )
    return RequirementCreateDTO(
        id=str(requirement.id),
        key=requirement.key,
        created_by_id=(
            str(requirement.created_by_id) if requirement.created_by_id else None
        ),
        title=requirement.title,
        description=requirement.description,
        feature_id=str(requirement.feature_id),
        target_release_version_id=None,
        implemented_release_version_id=None,
    )


@transaction.atomic
def requirement_update(
    *,
    project_id: str,
    requirement_id: str,
    user_id: str,
    title: str,
    description: str,
    target_release_version_id: str | None,
    implemented_release_version_id: str | None,
) -> RequirementUpdateDTO:
    """Update editable fields on a requirement.

    Args:
        project_id: Identifier of the project containing the requirement.
        requirement_id: Identifier of the requirement to update.
        user_id: Identifier of the user requesting the update.
        title: New requirement title.
        description: New requirement description.
        target_release_version_id: New target release identifier, or None to clear it.
        implemented_release_version_id: New implemented release identifier, or None
            to clear it.

    Returns:
        Serialized data for the updated requirement.

    Raises:
        RequirementUpdateForbiddenError: If the user cannot edit requirements.
        RequirementNotFoundError: If the requirement is not in the project.
        RequirementReleaseVersionNotFoundError: If a referenced release does not exist.
        RequirementTitleRequiredError: If the updated title is empty.
        RequirementDescriptionRequiredError: If the updated description is empty.
    """

    if not project_user_has_edit_permissions(project_id=project_id, user_id=user_id):
        raise RequirementUpdateForbiddenError(
            "Only project editors, moderators, and owners can update requirements."
        )

    requirement = (
        Requirement.objects.select_for_update()
        .filter(pk=requirement_id, feature__project_id=project_id, is_deleted=False)
        .first()
    )
    if requirement is None:
        raise RequirementNotFoundError(
            "Requirement does not exist in the selected project."
        )

    normalized_title = title.strip()
    if not normalized_title:
        raise RequirementTitleRequiredError("Requirement title cannot be empty.")
    normalized_description = description.strip()
    if not normalized_description:
        raise RequirementDescriptionRequiredError(
            "Requirement description cannot be empty."
        )

    release_versions: dict[str, ReleaseVersion | None] = {}
    for field_name, release_version_id in (
        ("target_release_version", target_release_version_id),
        ("implemented_release_version", implemented_release_version_id),
    ):
        if release_version_id is None:
            release_versions[field_name] = None
            continue
        try:
            release_versions[field_name] = ReleaseVersion.objects.get(
                pk=release_version_id
            )
        except ReleaseVersion.DoesNotExist as exc:
            raise RequirementReleaseVersionNotFoundError(
                "Release version does not exist."
            ) from exc

    requirement.title = normalized_title
    requirement.description = normalized_description
    requirement.target_release_version = release_versions["target_release_version"]
    requirement.implemented_release_version = release_versions[
        "implemented_release_version"
    ]
    requirement.save(
        update_fields=[
            "title",
            "description",
            "target_release_version",
            "implemented_release_version",
            "updated_at",
        ]
    )

    return RequirementUpdateDTO(
        id=str(requirement.id),
        key=requirement.key,
        created_by_id=str(requirement.created_by_id),
        title=requirement.title,
        description=requirement.description,
        feature_id=str(requirement.feature_id),
        target_release_version_id=(
            str(requirement.target_release_version_id)
            if requirement.target_release_version_id
            else None
        ),
        implemented_release_version_id=(
            str(requirement.implemented_release_version_id)
            if requirement.implemented_release_version_id
            else None
        ),
    )


@transaction.atomic
def requirement_delete(
    *, project_id: str, requirement_id: str, user_id: str
) -> RequirementDeleteDTO:
    """Soft-delete a requirement in a project.

    Args:
        project_id: Identifier of the project containing the requirement.
        requirement_id: Identifier of the requirement to delete.
        user_id: Identifier of the user requesting deletion.

    Returns:
        Serialized deletion result.

    Raises:
        RequirementDeleteForbiddenError: If the user cannot edit the project.
        RequirementNotFoundError: If the requirement is not active in the project.
    """

    if not project_user_has_edit_permissions(project_id=project_id, user_id=user_id):
        raise RequirementDeleteForbiddenError(
            "Only project editors, moderators, and owners can delete requirements."
        )

    requirement = (
        Requirement.objects.select_for_update()
        .filter(pk=requirement_id, feature__project_id=project_id, is_deleted=False)
        .first()
    )
    if requirement is None:
        raise RequirementNotFoundError(
            "Requirement does not exist in the selected project."
        )

    requirement.is_deleted = True
    requirement.save(update_fields=["is_deleted", "updated_at"])
    return RequirementDeleteDTO(id=str(requirement.id), is_deleted=True)
