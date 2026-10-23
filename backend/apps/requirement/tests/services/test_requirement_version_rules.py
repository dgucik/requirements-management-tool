import pytest
from django.contrib.auth import get_user_model

from apps.project.models import Project, ProjectMembership

from ...exceptions import (
    RequirementVersionNotApprovedError,
    RequirementVersionNotEditableError,
)
from ...models import Feature, Requirement, RequirementVersion
from ...services import requirement_version_create, requirement_version_update


@pytest.mark.django_db
def test_requirement_version_create_requires_approved_source():
    user = get_user_model().objects.create_user(username="version-author")
    project = Project.objects.create(name="Project", code="version-project")
    ProjectMembership.objects.create(
        user=user, project=project, role=ProjectMembership.Role.EDITOR
    )
    feature = Feature.objects.create(key="version-feature", title="Feature", project=project)
    requirement = Requirement.objects.create(key="version-requirement")
    source = RequirementVersion.objects.create(
        requirement=requirement,
        created_by=user,
        title="Draft title",
        description="Draft description",
        status=RequirementVersion.Status.DRAFT,
        version=1,
        feature=feature,
    )

    with pytest.raises(RequirementVersionNotApprovedError):
        requirement_version_create(
            project_id=str(project.id),
            requirement_id=str(requirement.id),
            based_on_version_id=str(source.id),
            user_id=str(user.id),
        )

    assert requirement.versions.count() == 1


@pytest.mark.django_db
def test_requirement_version_update_requires_draft_created_by_user():
    user = get_user_model().objects.create_user(username="version-owner")
    other_user = get_user_model().objects.create_user(username="other-version-user")
    project = Project.objects.create(name="Project", code="update-project")
    ProjectMembership.objects.create(
        user=user, project=project, role=ProjectMembership.Role.EDITOR
    )
    ProjectMembership.objects.create(
        user=other_user, project=project, role=ProjectMembership.Role.EDITOR
    )
    feature = Feature.objects.create(key="update-feature", title="Feature", project=project)
    requirement = Requirement.objects.create(key="update-requirement")
    version = RequirementVersion.objects.create(
        requirement=requirement,
        created_by=user,
        title="Original title",
        description="Original description",
        status=RequirementVersion.Status.DRAFT,
        version=1,
        feature=feature,
    )

    with pytest.raises(RequirementVersionNotEditableError):
        requirement_version_update(
            project_id=str(project.id),
            requirement_id=str(requirement.id),
            version_id=str(version.id),
            user_id=str(other_user.id),
            title="Updated title",
            description="Updated description",
            target_release_version_id=None,
            implemented_release_version_id=None,
            feature_id=str(feature.id),
        )

    version.refresh_from_db()
    assert version.title == "Original title"

