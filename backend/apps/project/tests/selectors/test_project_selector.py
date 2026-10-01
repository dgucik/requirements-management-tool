import pytest
from django.contrib.auth import get_user_model

from ...models import Project, ProjectMembership
from ...selectors import project_list


@pytest.mark.django_db
def test_project_list_returns_projects_with_user_membership():
    # Arrange
    user = get_user_model().objects.create_user(username="project-member")
    included_project = Project.objects.create(name="Included project")
    excluded_project = Project.objects.create(name="Excluded project")
    ProjectMembership.objects.create(
        user=user,
        project=included_project,
        role=ProjectMembership.Role.VIEWER,
    )

    # Act
    result = project_list(user_id=str(user.pk))

    # Assert
    assert [(project.id, project.name, project.role) for project in result] == [
        (str(included_project.id), included_project.name, ProjectMembership.Role.VIEWER)
    ]
    assert str(excluded_project.id) not in {project.id for project in result}
