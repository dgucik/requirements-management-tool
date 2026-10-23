import pytest
from django.contrib.auth import get_user_model

from apps.project.models import Project, ProjectMembership

from ...models import Feature, Requirement
from ...services import requirement_delete


@pytest.mark.django_db
def test_requirement_delete_sets_is_deleted_without_removing_row():
    user = get_user_model().objects.create_user(username="requirement-deleter")
    project = Project.objects.create(name="Project", code="requirement-delete")
    ProjectMembership.objects.create(
        user=user, project=project, role=ProjectMembership.Role.EDITOR
    )
    feature = Feature.objects.create(
        key="delete-feature", title="Feature", project=project
    )
    requirement = Requirement.objects.create(
        key="delete-requirement",
        created_by=user,
        title="Requirement",
        description="To be soft-deleted",
        feature=feature,
    )

    result = requirement_delete(
        project_id=str(project.id),
        requirement_id=str(requirement.id),
        user_id=str(user.id),
    )

    requirement.refresh_from_db()
    assert result.id == str(requirement.id)
    assert result.is_deleted is True
    assert requirement.is_deleted is True
    assert Requirement.objects.filter(pk=requirement.id).exists()
