import pytest
from django.contrib.auth import get_user_model

from apps.project.models import Project, ProjectMembership

from ...models import BusinessRule, Feature, Requirement
from ...services import business_rule_create, business_rule_delete, business_rule_update


@pytest.fixture
def business_rule_context():
    user = get_user_model().objects.create_user(username="business-rule-user")
    project = Project.objects.create(name="Project", code="business-rule")
    ProjectMembership.objects.create(
        user=user,
        project=project,
        role=ProjectMembership.Role.EDITOR,
    )
    feature = Feature.objects.create(
        key="business-rule-feature", title="Feature", project=project
    )
    requirement = Requirement.objects.create(
        key="business-rule-requirement",
        title="Requirement",
        description="Requirement description",
        feature=feature,
    )
    return user, project, requirement


@pytest.mark.django_db
def test_business_rule_create_assigns_project_requirements(business_rule_context):
    user, project, requirement = business_rule_context

    result = business_rule_create(
        project_id=str(project.id),
        user_id=str(user.id),
        rule="A valid session is required.",
        requirement_ids=[str(requirement.id)],
    )

    business_rule = BusinessRule.objects.get(pk=result.id)
    assert result.rule == business_rule.rule
    assert result.requirement_ids == [str(requirement.id)]
    assert list(business_rule.requirements.values_list("id", flat=True)) == [
        requirement.id
    ]


@pytest.mark.django_db
def test_business_rule_update_changes_rule_text(business_rule_context):
    user, project, requirement = business_rule_context
    business_rule = BusinessRule.objects.create(
        key="business-rule-update", rule="Old rule"
    )
    business_rule.requirements.add(requirement)

    result = business_rule_update(
        project_id=str(project.id),
        business_rule_id=str(business_rule.id),
        user_id=str(user.id),
        rule=" New rule ",
    )

    business_rule.refresh_from_db()
    assert result.rule == "New rule"
    assert business_rule.rule == "New rule"
    assert result.requirement_ids == [str(requirement.id)]


@pytest.mark.django_db
def test_business_rule_update_changes_requirement_assignments(business_rule_context):
    user, project, requirement = business_rule_context
    second_requirement = Requirement.objects.create(
        key="business-rule-second-requirement",
        title="Second requirement",
        description="Second description",
        feature=requirement.feature,
    )
    business_rule = BusinessRule.objects.create(
        key="business-rule-reassign", rule="Rule"
    )
    business_rule.requirements.add(requirement)

    result = business_rule_update(
        project_id=str(project.id),
        business_rule_id=str(business_rule.id),
        user_id=str(user.id),
        requirement_ids=[str(second_requirement.id)],
    )

    assert result.rule == "Rule"
    assert result.requirement_ids == [str(second_requirement.id)]
    assert list(business_rule.requirements.values_list("id", flat=True)) == [
        second_requirement.id
    ]


@pytest.mark.django_db
def test_business_rule_delete_is_soft_delete(business_rule_context):
    user, project, requirement = business_rule_context
    business_rule = BusinessRule.objects.create(
        key="business-rule-delete", rule="Rule"
    )
    business_rule.requirements.add(requirement)

    result = business_rule_delete(
        project_id=str(project.id),
        business_rule_id=str(business_rule.id),
        user_id=str(user.id),
    )

    business_rule.refresh_from_db()
    assert result.id == str(business_rule.id)
    assert result.is_deleted is True
    assert business_rule.is_deleted is True
    assert BusinessRule.objects.filter(pk=business_rule.id).exists()
