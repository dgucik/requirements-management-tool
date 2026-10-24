import pytest

from apps.project.models import Project

from ...models import BusinessRule, Feature, Requirement
from ...selectors import business_rule_list


@pytest.mark.django_db
def test_business_rule_list_returns_only_active_rules_for_project():
    project = Project.objects.create(name="Project", code="business-rule-list")
    feature = Feature.objects.create(
        key="business-rule-list-feature", title="Feature", project=project
    )
    requirement = Requirement.objects.create(
        key="business-rule-list-requirement",
        title="Requirement",
        description="Description",
        feature=feature,
    )
    active_rule = BusinessRule.objects.create(
        key="business-rule-list-active", rule="Active rule"
    )
    active_rule.requirements.add(requirement)
    deleted_rule = BusinessRule.objects.create(
        key="business-rule-list-deleted", rule="Deleted rule", is_deleted=True
    )
    deleted_rule.requirements.add(requirement)

    results = business_rule_list(project_id=str(project.id))

    assert [result.id for result in results] == [str(active_rule.id)]
    assert results[0].requirement_ids == [str(requirement.id)]
