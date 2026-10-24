from django.db import transaction

from apps.project.selectors import project_get, project_user_has_edit_permissions

from ..dtos import (
    BusinessRuleCreateDTO,
    BusinessRuleDeleteDTO,
    BusinessRuleUpdateDTO,
)
from ..exceptions import (
    BusinessRuleCreationForbiddenError,
    BusinessRuleDeleteForbiddenError,
    BusinessRuleNotFoundError,
    BusinessRuleTextRequiredError,
    BusinessRuleUpdateForbiddenError,
)
from ..identifiers import requirement_key_generate
from ..models import BusinessRule
from ..selectors import (
    business_rule_requirement_id_list,
    key_existing_list,
    requirement_active_id_list,
)


@transaction.atomic
def business_rule_create(
    *, project_id: str, user_id: str, rule: str, requirement_ids: list[str]
) -> BusinessRuleCreateDTO:
    """Create a business rule associated with project requirements.

    Args:
        project_id: Identifier of the project receiving the rule.
        user_id: Identifier of the user creating the rule.
        rule: Business rule text.
        requirement_ids: Active requirement identifiers in the project.

    Returns:
        Serialized data for the created business rule.
    """

    project_get(project_id=project_id)
    if not project_user_has_edit_permissions(project_id=project_id, user_id=user_id):
        raise BusinessRuleCreationForbiddenError(
            "Only project editors, moderators, and owners can create business rules."
        )

    normalized_rule = rule.strip()
    if not normalized_rule:
        raise BusinessRuleTextRequiredError("Business rule cannot be empty.")
    valid_requirement_ids = requirement_active_id_list(
        project_id=project_id,
        requirement_ids=requirement_ids,
    )

    business_rule = BusinessRule.objects.create(
        key=requirement_key_generate(
            project_code=project_get(project_id=project_id).code,
            existing_keys=key_existing_list(),
        ),
        rule=normalized_rule,
    )
    business_rule.requirements.set(valid_requirement_ids)
    return BusinessRuleCreateDTO(
        id=str(business_rule.id),
        key=business_rule.key,
        rule=business_rule.rule,
        requirement_ids=valid_requirement_ids,
    )


@transaction.atomic
def business_rule_update(
    *,
    project_id: str,
    business_rule_id: str,
    user_id: str,
    rule: str | None = None,
    requirement_ids: list[str] | None = None,
) -> BusinessRuleUpdateDTO:
    """Update editable fields of an active project business rule.

    Args:
        project_id: Identifier of the project containing the rule.
        business_rule_id: Identifier of the rule to update.
        user_id: Identifier of the user requesting the update.
        rule: New business rule text, or None to leave it unchanged.
        requirement_ids: New active project requirement identifiers, or None to
            leave the current assignments unchanged.

    Returns:
        Serialized data for the updated business rule.
    """

    if not project_user_has_edit_permissions(project_id=project_id, user_id=user_id):
        raise BusinessRuleUpdateForbiddenError(
            "Only project editors, moderators, and owners can update business rules."
        )
    if rule is None and requirement_ids is None:
        raise BusinessRuleTextRequiredError(
            "At least one business rule field must be provided."
        )
    normalized_rule = rule.strip() if rule is not None else None
    if rule is not None and not normalized_rule:
        raise BusinessRuleTextRequiredError("Business rule cannot be empty.")

    business_rule = (
        BusinessRule.objects.select_for_update()
        .filter(
            id=business_rule_id,
            is_deleted=False,
            requirements__feature__project_id=project_id,
            requirements__feature__is_deleted=False,
            requirements__is_deleted=False,
        )
        .distinct()
        .first()
    )
    if business_rule is None:
        raise BusinessRuleNotFoundError(
            "Business rule does not exist in the selected project."
        )

    update_fields = ["updated_at"]
    if normalized_rule is not None:
        business_rule.rule = normalized_rule
        update_fields.append("rule")
    business_rule.save(update_fields=update_fields)
    updated_requirement_ids = business_rule_requirement_id_list(
        business_rule_id=str(business_rule.id),
        project_id=project_id,
    )
    if requirement_ids is not None:
        updated_requirement_ids = requirement_active_id_list(
            project_id=project_id,
            requirement_ids=requirement_ids,
        )
        business_rule.requirements.set(updated_requirement_ids)
    return BusinessRuleUpdateDTO(
        id=str(business_rule.id),
        key=business_rule.key,
        rule=business_rule.rule,
        requirement_ids=updated_requirement_ids,
    )


@transaction.atomic
def business_rule_delete(
    *, project_id: str, business_rule_id: str, user_id: str
) -> BusinessRuleDeleteDTO:
    """Soft-delete an active project business rule.

    Args:
        project_id: Identifier of the project containing the rule.
        business_rule_id: Identifier of the rule to delete.
        user_id: Identifier of the user requesting deletion.

    Returns:
        Serialized deletion result.
    """

    if not project_user_has_edit_permissions(project_id=project_id, user_id=user_id):
        raise BusinessRuleDeleteForbiddenError(
            "Only project editors, moderators, and owners can delete business rules."
        )

    business_rule = (
        BusinessRule.objects.select_for_update()
        .filter(
            id=business_rule_id,
            is_deleted=False,
            requirements__feature__project_id=project_id,
            requirements__feature__is_deleted=False,
            requirements__is_deleted=False,
        )
        .distinct()
        .first()
    )
    if business_rule is None:
        raise BusinessRuleNotFoundError(
            "Business rule does not exist in the selected project."
        )

    business_rule.is_deleted = True
    business_rule.save(update_fields=["is_deleted", "updated_at"])
    return BusinessRuleDeleteDTO(id=str(business_rule.id), is_deleted=True)
