from django.db import transaction

from apps.project.selectors import project_get, project_user_has_edit_permissions

from ..dtos import FeatureCreateDTO, FeatureDeleteDTO, FeatureUpdateDTO
from ..exceptions import (
    FeatureCreationForbiddenError,
    FeatureDeleteForbiddenError,
    FeatureNotFoundError,
    FeatureTitleRequiredError,
    FeatureUpdateForbiddenError,
)
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


@transaction.atomic
def feature_update(
    *, project_id: str, feature_id: str, user_id: str, title: str
) -> FeatureUpdateDTO:
    """Update the title of an active project feature.

    Args:
        project_id: Identifier of the project containing the feature.
        feature_id: Identifier of the feature to update.
        user_id: Identifier of the user requesting the update.
        title: New feature title.

    Returns:
        Serialized data for the updated feature.

    Raises:
        FeatureUpdateForbiddenError: If the user cannot edit the project.
        FeatureNotFoundError: If the feature is not active in the project.
        FeatureTitleRequiredError: If the title is empty after trimming.
    """

    if not project_user_has_edit_permissions(project_id=project_id, user_id=user_id):
        raise FeatureUpdateForbiddenError(
            "Only project editors, moderators, and owners can update features."
        )

    normalized_title = title.strip()
    if not normalized_title:
        raise FeatureTitleRequiredError("Feature title cannot be empty.")

    feature = (
        Feature.objects.select_for_update()
        .filter(pk=feature_id, project_id=project_id, is_deleted=False)
        .first()
    )
    if feature is None:
        raise FeatureNotFoundError("Feature does not exist in the selected project.")

    feature.title = normalized_title
    feature.save(update_fields=["title", "updated_at"])
    return FeatureUpdateDTO(
        id=str(feature.id),
        key=feature.key,
        title=feature.title,
        project_id=str(feature.project_id),
    )


@transaction.atomic
def feature_delete(
    *, project_id: str, feature_id: str, user_id: str
) -> FeatureDeleteDTO:
    """Soft-delete an active project feature.

    Args:
        project_id: Identifier of the project containing the feature.
        feature_id: Identifier of the feature to delete.
        user_id: Identifier of the user requesting deletion.

    Returns:
        Serialized deletion result.

    Raises:
        FeatureDeleteForbiddenError: If the user cannot edit the project.
        FeatureNotFoundError: If the feature is not active in the project.
    """

    if not project_user_has_edit_permissions(project_id=project_id, user_id=user_id):
        raise FeatureDeleteForbiddenError(
            "Only project editors, moderators, and owners can delete features."
        )

    feature = (
        Feature.objects.select_for_update()
        .filter(pk=feature_id, project_id=project_id, is_deleted=False)
        .first()
    )
    if feature is None:
        raise FeatureNotFoundError("Feature does not exist in the selected project.")

    feature.is_deleted = True
    feature.save(update_fields=["is_deleted", "updated_at"])
    return FeatureDeleteDTO(id=str(feature.id), is_deleted=True)
