from itertools import chain

from .dtos import FeatureListDTO, RequirementListDTO
from .models import BusinessRule, Feature, Requirement


def feature_list(*, project_id: str) -> list[FeatureListDTO]:
    """Return all features assigned to a project.

    Args:
        project_id: Identifier of the project whose features are listed.

    Returns:
        Features belonging to the project, ordered by key.
    """

    features = (
        Feature.objects.filter(project_id=project_id, is_deleted=False)
        .order_by("key")
        .values("id", "key", "title", "project_id")
    )

    return [
        FeatureListDTO(
            id=str(row["id"]),
            key=row["key"],
            title=row["title"],
            project_id=str(row["project_id"]),
        )
        for row in features
    ]


def key_existing_list() -> list[str]:
    """Return keys used by requirements, business rules, and features.

    Returns:
        A sorted list of unique keys used by supported requirement items.
    """

    key_querysets = (
        Requirement.objects.values_list("key", flat=True),
        BusinessRule.objects.values_list("key", flat=True),
        Feature.objects.values_list("key", flat=True),
    )
    return sorted(set(chain.from_iterable(key_querysets)))


def requirement_list(*, project_id: str) -> list[RequirementListDTO]:
    """Return all non-deleted requirements in a project.

    Args:
        project_id: Identifier of the project whose requirements are listed.
    Returns:
        Flat requirement data ordered by requirement key.
    """

    requirements = (
        Requirement.objects.filter(
            feature__project_id=project_id,
            feature__is_deleted=False,
            is_deleted=False,
        )
        .order_by("key")
        .values(
            "id",
            "key",
            "created_by_id",
            "title",
            "description",
            "feature_id",
            "target_release_version_id",
            "implemented_release_version_id",
        )
    )

    return [
        RequirementListDTO(
            id=str(row["id"]),
            key=row["key"],
            created_by_id=(
                str(row["created_by_id"]) if row["created_by_id"] else None
            ),
            title=row["title"],
            description=row["description"],
            feature_id=str(row["feature_id"]),
            target_release_version_id=(
                str(row["target_release_version_id"])
                if row["target_release_version_id"]
                else None
            ),
            implemented_release_version_id=(
                str(row["implemented_release_version_id"])
                if row["implemented_release_version_id"]
                else None
            ),
        )
        for row in requirements
    ]
