from django.db import transaction

from apps.project.models import Project
from apps.project.selectors import project_user_can_create_requirement

from ..dtos import RequirementCreateDTO, RequirementVersionCreateDTO
from ..exceptions import (
    RequirementCreationForbiddenError,
    RequirementDescriptionRequiredError,
    RequirementFeatureNotFoundError,
    RequirementTitleRequiredError,
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
    )

    return RequirementCreateDTO(
        id=str(requirement.id),
        key=requirement.key,
        first_version=RequirementVersionCreateDTO(
            id=str(first_version.id),
            requirement_id=str(requirement.id),
            title=first_version.title,
            description=first_version.description,
            status=first_version.status,
            version=first_version.version,
            feature_id=str(feature.id),
        ),
    )
