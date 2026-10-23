from itertools import chain

from django.db.models import F, OuterRef, Q, Subquery

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


def requirement_list(*, project_id: str, user_id: str) -> list[RequirementListDTO]:
    """Return project requirements with their latest non-deleted version.

    Args:
        project_id: Identifier of the project whose requirements are listed.
        user_id: Identifier of the user requesting the list.

    Returns:
        Flat requirement and version data, ordered by requirement key. Requirements
        without a non-deleted version in the project are omitted.
    """

    # TODO: This should eventually select the latest approved version, not the
    # version with the highest version number.
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
        .filter(
            ~Q(status=RequirementVersion.Status.DRAFT)
            | Q(created_by_id=user_id)
        )
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


def requirement_version_can_be_edited(
    *, project_id: str, requirement_id: str, version_id: str, user_id: str
) -> bool:
    """Check whether a user can edit an active draft requirement version.

    Args:
        project_id: Identifier of the project containing the version.
        requirement_id: Identifier of the requirement containing the version.
        version_id: Identifier of the version to check.
        user_id: Identifier of the user requesting the edit.

    Returns:
        True if the version is a non-deleted draft in the project and was created
        by the requesting user.
    """

    return RequirementVersion.objects.filter(
        pk=version_id,
        requirement_id=requirement_id,
        feature__project_id=project_id,
        is_deleted=False,
        status=RequirementVersion.Status.DRAFT,
        created_by_id=user_id,
    ).exists()
