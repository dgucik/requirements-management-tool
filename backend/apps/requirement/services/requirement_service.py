from django.db import transaction
from django.db.models import Max

from apps.project.models import Project
from apps.project.selectors import project_user_can_create_requirement

from ..dtos import (
    RequirementCreateDTO,
    RequirementInitialVersionDTO,
    RequirementVersionCreateDTO,
)
from ..exceptions import (
    RequirementCreationForbiddenError,
    RequirementDescriptionRequiredError,
    RequirementFeatureNotFoundError,
    RequirementNotFoundError,
    RequirementTitleRequiredError,
    RequirementVersionNotFoundError,
)
from ..identifiers import requirement_key_generate
from ..models import Feature, Requirement, RequirementVersion


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

    if not project_user_can_create_requirement(
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
        existing_keys=Requirement.objects.values_list("key", flat=True),
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
        first_version=RequirementInitialVersionDTO(
            id=str(first_version.id),
            requirement_id=str(requirement.id),
            based_on_version_id=None,
            created_by_id=str(user_id),
            title=first_version.title,
            description=first_version.description,
            status=first_version.status,
            version=first_version.version,
            feature_id=str(feature.id),
            target_release_version_id=None,
            implemented_release_version_id=None,
        ),
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

    if not project_user_can_create_requirement(
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
