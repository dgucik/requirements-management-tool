from django.db import transaction

from apps.project.selectors import project_get, project_user_has_edit_permissions

from ..dtos import FeatureCreateDTO
from ..exceptions import FeatureCreationForbiddenError, FeatureTitleRequiredError
from ..identifiers import requirement_key_generate
from ..models import Feature
from ..selectors import key_existing_list


@transaction.atomic
def feature_create(
    *, project_id: str, user_id: str, title: str
) -> FeatureCreateDTO:
    """Create a feature in a project with a shared project key.

    Args:
        project_id: Identifier of the project receiving the feature.
        user_id: Identifier of the user creating the feature.
        title: Display title for the feature.

    Returns:
        Serialized data for the created feature.

    Raises:
        ProjectNotFoundError: If the project does not exist.
        FeatureCreationForbiddenError: If the user cannot create project features.
        FeatureTitleRequiredError: If the title is empty after trimming.
    """

    normalized_title = title.strip()
    if not normalized_title:
        raise FeatureTitleRequiredError("Feature title cannot be empty.")

    project = project_get(project_id=project_id)

    if not project_user_has_edit_permissions(
        project_id=project_id,
        user_id=user_id,
    ):
        raise FeatureCreationForbiddenError(
            "Only project editors, moderators, and owners can create features."
        )

    feature = Feature.objects.create(
        key=requirement_key_generate(
            project_code=project.code,
            existing_keys=key_existing_list(),
        ),
        title=normalized_title,
        project_id=project.id,
    )

    return FeatureCreateDTO(
        id=str(feature.id),
        key=feature.key,
        title=feature.title,
        project_id=project.id,
    )
