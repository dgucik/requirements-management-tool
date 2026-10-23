import pytest
from django.contrib.auth import get_user_model

from apps.project.models import Project, ProjectMembership

from ...models import Feature, Requirement
from ...services import requirement_update


@pytest.mark.django_db
def test_requirement_update_changes_flat_requirement_fields():
    user = get_user_model().objects.create_user(username="requirement-editor")
    project = Project.objects.create(name="Project", code="requirement-update")
    ProjectMembership.objects.create(
        user=user, project=project, role=ProjectMembership.Role.EDITOR
    )
    old_feature = Feature.objects.create(
        key="old-feature", title="Old feature", project=project
    )
    requirement = Requirement.objects.create(
        key="requirement-update-1",
        created_by=user,
        title="Old title",
        description="Old description",
        feature=old_feature,
    )

    result = requirement_update(
        project_id=str(project.id),
        requirement_id=str(requirement.id),
        user_id=str(user.id),
        title="New title",
        description="New description",
        target_release_version_id=None,
        implemented_release_version_id=None,
    )

    requirement.refresh_from_db()
    assert result.id == str(requirement.id)
    assert result.title == "New title"
    assert requirement.title == "New title"
    assert requirement.description == "New description"
    assert requirement.feature_id == old_feature.id
