from itertools import chain

from django.db.models import Prefetch

from .dtos import BusinessRuleListDTO, FeatureListDTO, RequirementListDTO
from .exceptions import BusinessRuleRequirementsNotFoundError
from .models import BusinessRule, Feature, Requirement


def requirement_active_id_list(
    *, project_id: str, requirement_ids: list[str]
) -> list[str]:
    """Return validated active requirement identifiers for a project.

    Args:
        project_id: Identifier of the project containing the requirements.
        requirement_ids: Requirement identifiers to validate.

    Returns:
        De-duplicated requirement identifiers in input order.

    Raises:
        BusinessRuleRequirementsNotFoundError: If any requirement is not active
            in the project.
    """

    normalized_ids = list(dict.fromkeys(requirement_ids))
    matching_ids = {
        str(requirement_id)
        for requirement_id in Requirement.objects.filter(
            id__in=normalized_ids,
            feature__project_id=project_id,
            feature__is_deleted=False,
            is_deleted=False,
        ).values_list("id", flat=True)
    }
    if not normalized_ids or matching_ids != set(normalized_ids):
        raise BusinessRuleRequirementsNotFoundError(
            "All business rule requirements must be active and belong to the project."
        )
    return normalized_ids


def business_rule_requirement_id_list(
    *, business_rule_id: str, project_id: str
) -> list[str]:
    """Return active project requirement identifiers assigned to a rule.

    Args:
        business_rule_id: Identifier of the business rule.
        project_id: Identifier of the project containing the requirements.

    Returns:
        Active requirement identifiers assigned to the rule.
    """

    return [
        str(requirement_id)
        for requirement_id in Requirement.objects.filter(
            business_rules__id=business_rule_id,
            feature__project_id=project_id,
            feature__is_deleted=False,
            is_deleted=False,
        ).values_list("id", flat=True)
    ]


def business_rule_list(*, project_id: str) -> list[BusinessRuleListDTO]:
    """Return active business rules associated with active project requirements.

    Args:
        project_id: Identifier of the project whose business rules are listed.

    Returns:
        Business rules ordered by key, including their requirement identifiers.
    """

    business_rules = (
        BusinessRule.objects.filter(
            is_deleted=False,
            requirements__feature__project_id=project_id,
            requirements__feature__is_deleted=False,
            requirements__is_deleted=False,
        )
        .distinct()
        .prefetch_related(
            Prefetch(
                "requirements",
                queryset=Requirement.objects.filter(
                    feature__project_id=project_id,
                    feature__is_deleted=False,
                    is_deleted=False,
                ).select_related("feature"),
                to_attr="active_project_requirements",
            )
        )
        .order_by("key")
    )

    return [
        BusinessRuleListDTO(
            id=str(business_rule.id),
            key=business_rule.key,
            rule=business_rule.rule,
            requirement_ids=[
                str(requirement.id)
                for requirement in business_rule.active_project_requirements
            ],
        )
        for business_rule in business_rules
    ]


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
