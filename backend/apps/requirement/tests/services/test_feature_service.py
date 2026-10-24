import pytest
from django.contrib.auth import get_user_model

from apps.project.models import Project, ProjectMembership

from ...models import Feature
from ...services import feature_delete, feature_update


@pytest.mark.django_db
def test_feature_update_changes_only_title():
    user = get_user_model().objects.create_user(username="feature-updater")
    project = Project.objects.create(name="Project", code="feature-update")
    ProjectMembership.objects.create(
        user=user,
        project=project,
        role=ProjectMembership.Role.EDITOR,
    )
    feature = Feature.objects.create(
        key="feature-update-key", title="Old title", project=project
    )

    result = feature_update(
        project_id=str(project.id),
        feature_id=str(feature.id),
        user_id=str(user.id),
        title=" New title ",
    )

    feature.refresh_from_db()
    assert result.title == "New title"
    assert feature.title == "New title"
    assert feature.key == "feature-update-key"
    assert feature.is_deleted is False


@pytest.mark.django_db
def test_feature_delete_sets_is_deleted_without_removing_row():
    user = get_user_model().objects.create_user(username="feature-deleter")
    project = Project.objects.create(name="Project", code="feature-delete")
    ProjectMembership.objects.create(
        user=user,
        project=project,
        role=ProjectMembership.Role.EDITOR,
    )
    feature = Feature.objects.create(
        key="feature-delete-key", title="Feature", project=project
    )

    result = feature_delete(
        project_id=str(project.id),
        feature_id=str(feature.id),
        user_id=str(user.id),
    )

    feature.refresh_from_db()
    assert result.id == str(feature.id)
    assert result.is_deleted is True
    assert feature.is_deleted is True
    assert Feature.objects.filter(pk=feature.id).exists()
