import pytest
from django.contrib.auth import get_user_model

from apps.project.models import Project, ProjectMembership
from apps.project.selectors import project_user_has_edit_permissions


@pytest.mark.django_db
@pytest.mark.parametrize(
    "role, expected",
    [
        (ProjectMembership.Role.EDITOR, True),
        (ProjectMembership.Role.MODERATOR, True),
        (ProjectMembership.Role.OWNER, True),
        (ProjectMembership.Role.VIEWER, False),
    ],
)
def test_project_user_has_edit_permissions(role, expected):
    user = get_user_model().objects.create_user(username=f"{role}-user")
    project = Project.objects.create(name="Requirements Tool", code=f"p-{role.lower()}")
    ProjectMembership.objects.create(user=user, project=project, role=role)

    assert (
        project_user_has_edit_permissions(
            project_id=str(project.id),
            user_id=str(user.id),
        )
        is expected
    )
