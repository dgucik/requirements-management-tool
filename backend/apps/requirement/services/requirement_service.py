from django.db import transaction
from django.db.models import Max

from apps.project.models import Project
from apps.project.selectors import project_user_has_edit_permissions

from ..dtos import (
    RequirementCreateDTO,
    RequirementVersionCreateDTO,
    RequirementVersionUpdateDTO,
)
from ..exceptions import (
    RequirementCreationForbiddenError,
    RequirementDescriptionRequiredError,
    RequirementFeatureNotFoundError,
    RequirementNotFoundError,
    RequirementReleaseVersionNotFoundError,
    RequirementTitleRequiredError,
    RequirementVersionNotEditableError,
    RequirementVersionNotFoundError,
    RequirementVersionNotApprovedError,
    RequirementVersionUpdateForbiddenError,
)
from ..identifiers import requirement_key_generate
from ..models import Feature, ReleaseVersion, Requirement, RequirementVersion
from ..selectors import key_existing_list, requirement_version_can_be_edited


@transaction.atomic
def requirement_create(
    *,
    project_id: str,
    user_id: str,
    title: str,
    description: str,
    feature_id: str,
) -> RequirementCreateDTO:
    """Create a requirement and its first draft version.

    Args:
        project_id: Identifier of the project receiving the requirement.
        user_id: Identifier of the user creating the requirement.
        title: Title of the first requirement version.
        description: Description of the first requirement version.
        feature_id: Identifier of the feature assigned to the first version.

    Returns:
        Serialized requirement data including its first version.

    Raises:
        RequirementCreationForbiddenError: If the user lacks the required project role.
        RequirementFeatureNotFoundError: If the feature is not in the project.
        RequirementTitleRequiredError: If the title is empty after trimming.
        RequirementDescriptionRequiredError: If the description is empty after trimming.
    """

    if not project_user_has_edit_permissions(
        project_id=project_id,
        user_id=user_id,
    ):
        raise RequirementCreationForbiddenError(
            "Only project editors, moderators, and owners can create requirements."
        )

    normalized_title = title.strip()
    if not normalized_title:
        raise RequirementTitleRequiredError(
            "Requirement title cannot be empty."
        )

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

    requirement_key = requirement_key_generate(
        project_code=project.code,
        existing_keys=key_existing_list(),
    )
    requirement = Requirement.objects.create(key=requirement_key)
    first_version = RequirementVersion.objects.create(
        requirement=requirement,
        title=normalized_title,
        description=normalized_description,
        status=RequirementVersion.Status.DRAFT,
        version=1,
        feature=feature,
        created_by_id=user_id,
    )

    return RequirementCreateDTO(
        id=str(requirement.id),
        key=requirement.key,
        version_id=str(first_version.id),
        based_on_version_id=None,
        created_by_id=str(user_id),
        title=first_version.title,
        description=first_version.description,
        status=first_version.status,
        version=first_version.version,
        feature_id=str(feature.id),
        target_release_version_id=None,
        implemented_release_version_id=None,
    )


@transaction.atomic
def requirement_version_create(
    *,
    project_id: str,
    requirement_id: str,
    based_on_version_id: str,
    user_id: str,
) -> RequirementVersionCreateDTO:
    """Create a draft version by copying an existing version.

    Args:
        project_id: Identifier of the project containing the requirement.
        requirement_id: Identifier of the requirement receiving the new version.
        based_on_version_id: Identifier of the version to copy.
        user_id: Identifier of the user creating the version.

    Returns:
        Serialized data for the new draft version.

    Raises:
        RequirementCreationForbiddenError: If the user lacks a permitted project role.
        RequirementNotFoundError: If the requirement does not belong to the project.
        RequirementVersionNotFoundError: If the source version is not in the requirement.
    """

    if not project_user_has_edit_permissions(
        project_id=project_id,
        user_id=user_id,
    ):
        raise RequirementCreationForbiddenError(
            "Only project editors, moderators, and owners can create requirement versions."
        )

    requirement = (
        Requirement.objects.select_for_update()
        .filter(
            pk=requirement_id,
            versions__feature__project_id=project_id,
        )
        .first()
    )
    if requirement is None:
        raise RequirementNotFoundError(
            "Requirement does not exist in the selected project."
        )

    try:
        source_version = RequirementVersion.objects.get(
            pk=based_on_version_id,
            requirement=requirement,
            is_deleted=False,
        )
    except RequirementVersion.DoesNotExist as exc:
        raise RequirementVersionNotFoundError(
            "Source version does not exist for this requirement."
        ) from exc

    if source_version.status != RequirementVersion.Status.APPROVED:
        raise RequirementVersionNotApprovedError(
            "New requirement versions can only be based on approved versions."
        )

    latest_number = RequirementVersion.objects.filter(
        requirement=requirement,
    ).aggregate(max_version=Max("version"))["max_version"] or 0
    new_version = RequirementVersion.objects.create(
        requirement=requirement,
        based_on_version=source_version,
        created_by_id=user_id,
        title=source_version.title,
        description=source_version.description,
        target_release_version=source_version.target_release_version,
        implemented_release_version=source_version.implemented_release_version,
        status=RequirementVersion.Status.DRAFT,
        version=latest_number + 1,
        feature=source_version.feature,
        is_deleted=False,
    )

    return RequirementVersionCreateDTO(
        id=str(new_version.id),
        requirement_id=str(requirement.id),
        based_on_version_id=str(source_version.id),
        created_by_id=str(user_id),
        title=new_version.title,
        description=new_version.description,
        status=new_version.status,
        version=new_version.version,
        feature_id=str(new_version.feature_id),
        target_release_version_id=(
            str(new_version.target_release_version_id)
            if new_version.target_release_version_id
            else None
        ),
        implemented_release_version_id=(
            str(new_version.implemented_release_version_id)
            if new_version.implemented_release_version_id
            else None
        ),
    )


@transaction.atomic
def requirement_version_update(
    *,
    project_id: str,
    requirement_id: str,
    version_id: str,
    user_id: str,
    title: str,
    description: str,
    target_release_version_id: str | None,
    implemented_release_version_id: str | None,
    feature_id: str,
) -> RequirementVersionUpdateDTO:
    """Update editable fields on a requirement version.

    Args:
        project_id: Identifier of the project containing the requirement.
        requirement_id: Identifier of the requirement being updated.
        version_id: Identifier of the version to update.
        user_id: Identifier of the user requesting the update.
        title: New title for the requirement version.
        description: New description for the requirement version.
        target_release_version_id: New target release identifier, or None to clear it.
        implemented_release_version_id: New implemented release identifier, or None
            to clear it.
        feature_id: Identifier of the feature assigned to the version.

    Returns:
        Serialized data for the updated requirement version.

    Raises:
        RequirementVersionUpdateForbiddenError: If the user cannot edit requirements.
        RequirementNotFoundError: If the requirement is not in the project.
        RequirementVersionNotFoundError: If the version is inactive or outside the project.
        RequirementVersionNotEditableError: If the version is not a draft created by
            the requesting user.
        RequirementFeatureNotFoundError: If the feature is not in the project.
        RequirementReleaseVersionNotFoundError: If a referenced release does not exist.
        RequirementTitleRequiredError: If the updated title is empty.
        RequirementDescriptionRequiredError: If the updated description is empty.
    """

    if not project_user_has_edit_permissions(
        project_id=project_id,
        user_id=user_id,
    ):
        raise RequirementVersionUpdateForbiddenError(
            "Only project editors, moderators, and owners can update requirement versions."
        )

    version = (
        RequirementVersion.objects.select_related("requirement").select_for_update()
        .filter(
            pk=version_id,
            requirement_id=requirement_id,
            feature__project_id=project_id,
            is_deleted=False,
        )
        .first()
    )
    if version is None:
        if not Requirement.objects.filter(
            pk=requirement_id,
            versions__feature__project_id=project_id,
        ).exists():
            raise RequirementNotFoundError(
                "Requirement does not exist in the selected project."
            )
        raise RequirementVersionNotFoundError(
            "Requirement version does not exist or has been deleted."
        )

    if not requirement_version_can_be_edited(
        project_id=project_id,
        requirement_id=requirement_id,
        version_id=version_id,
        user_id=user_id,
    ):
        raise RequirementVersionNotEditableError(
            "Only draft requirement versions can be edited."
        )

    normalized_title = title.strip()
    if not normalized_title:
        raise RequirementTitleRequiredError("Requirement title cannot be empty.")
    normalized_description = description.strip()
    if not normalized_description:
        raise RequirementDescriptionRequiredError(
            "Requirement description cannot be empty."
        )

    try:
        feature = Feature.objects.get(pk=feature_id, project_id=project_id)
    except Feature.DoesNotExist as exc:
        raise RequirementFeatureNotFoundError(
            "Feature does not exist in the selected project."
        ) from exc

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

    version.title = normalized_title
    version.description = normalized_description
    version.feature = feature
    version.target_release_version = release_versions["target_release_version"]
    version.implemented_release_version = release_versions[
        "implemented_release_version"
    ]
    version.save(
        update_fields=[
            "title",
            "description",
            "feature",
            "target_release_version",
            "implemented_release_version",
            "updated_at",
        ]
    )

    return RequirementVersionUpdateDTO(
        id=str(version.id),
        requirement_id=str(version.requirement_id),
        based_on_version_id=(
            str(version.based_on_version_id)
            if version.based_on_version_id
            else None
        ),
        created_by_id=(
            str(version.created_by_id) if version.created_by_id else None
        ),
        title=version.title,
        description=version.description,
        status=version.status,
        version=version.version,
        feature_id=str(version.feature_id),
        target_release_version_id=(
            str(version.target_release_version_id)
            if version.target_release_version_id
            else None
        ),
        implemented_release_version_id=(
            str(version.implemented_release_version_id)
            if version.implemented_release_version_id
            else None
        ),
    )
