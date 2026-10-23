from itertools import chain

from django.db.models import F, OuterRef, Subquery

from .dtos import RequirementListDTO
from .models import BusinessRule, Feature, Requirement
from .models import RequirementVersion


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
    """Return project requirements with their latest non-deleted version.

    Args:
        project_id: Identifier of the project whose requirements are listed.

    Returns:
        Flat requirement and version data, ordered by requirement key. Requirements
        without a non-deleted version in the project are omitted.
    """

    latest_active_version = (
        RequirementVersion.objects.filter(
            requirement_id=OuterRef("requirement_id"),
            is_deleted=False,
        )
        .order_by("-version")
        .values("version")[:1]
    )
    versions = (
        RequirementVersion.objects.filter(
            feature__project_id=project_id,
            is_deleted=False,
        )
        .annotate(latest_active_version=Subquery(latest_active_version))
        .filter(version=F("latest_active_version"))
        .order_by("requirement__key")
        .values(
            "requirement_id",
            "requirement__key",
            "id",
            "based_on_version_id",
            "created_by_id",
            "title",
            "description",
            "status",
            "version",
            "feature_id",
            "target_release_version_id",
            "implemented_release_version_id",
        )
    )

    return [
        RequirementListDTO(
            id=str(row["requirement_id"]),
            key=row["requirement__key"],
            version_id=str(row["id"]),
            based_on_version_id=(
                str(row["based_on_version_id"])
                if row["based_on_version_id"]
                else None
            ),
            created_by_id=(
                str(row["created_by_id"]) if row["created_by_id"] else None
            ),
            title=row["title"],
            description=row["description"],
            status=row["status"],
            version=row["version"],
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
        for row in versions
    ]
