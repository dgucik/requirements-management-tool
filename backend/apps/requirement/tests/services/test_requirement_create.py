import pytest
from django.contrib.auth import get_user_model

from apps.project.models import Project, ProjectMembership

from ...exceptions import RequirementCreationForbiddenError
from ...models import Feature, Requirement, RequirementVersion
from ...services import requirement_create


@pytest.mark.django_db
@pytest.mark.parametrize(
    "role",
    [
        ProjectMembership.Role.EDITOR,
        ProjectMembership.Role.MODERATOR,
        ProjectMembership.Role.OWNER,
    ],
)
def test_requirement_create_allows_project_management_roles(role):
    user = get_user_model().objects.create_user(username=f"{role}-user")
    project = Project.objects.create(name="Requirements Tool", code=f"p-{role.lower()}")
    ProjectMembership.objects.create(user=user, project=project, role=role)

    feature = Feature.objects.create(
        key=f"feature-{role.lower()}",
        title="Login",
        project=project,
    )

    result = requirement_create(
        project_id=str(project.id),
        user_id=str(user.id),
        title="Login flow",
        description="Users can log in.",
        feature_id=str(feature.id),
    )

    requirement = Requirement.objects.get(id=result.id)
    version = RequirementVersion.objects.get(requirement=requirement)
    assert result.key == f"p-{role.lower()}-r-1"
    assert requirement.key == result.key
    assert version.title == "Login flow"
    assert version.description == "Users can log in."
    assert version.status == RequirementVersion.Status.DRAFT
    assert version.version == 1


@pytest.mark.django_db
def test_requirement_create_rejects_viewer():
    user = get_user_model().objects.create_user(username="viewer-user")
    project = Project.objects.create(name="Requirements Tool", code="p-viewer")
    ProjectMembership.objects.create(
        user=user,
        project=project,
        role=ProjectMembership.Role.VIEWER,
    )

    feature = Feature.objects.create(
        key="feature-viewer",
        title="Login",
        project=project,
    )

    with pytest.raises(RequirementCreationForbiddenError):
        requirement_create(
            project_id=str(project.id),
            user_id=str(user.id),
            title="Login flow",
            description="Users can log in.",
            feature_id=str(feature.id),
        )

    assert Requirement.objects.count() == 0
