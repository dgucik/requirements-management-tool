from ..dtos import ProjectMembershipListDTO
from ..exceptions import ProjectNotFoundError
from ..models import Project, ProjectMembership


def project_membership_list(*, project_id: str) -> list[ProjectMembershipListDTO]:
    """Return all memberships assigned to a project.

    Args:
        project_id: Identifier of the project whose memberships should be returned.

    Returns:
        Memberships assigned to the project, including their roles.

    Raises:
        ProjectNotFoundError: If the project does not exist.
    """

    if not Project.objects.filter(id=project_id).exists():
        raise ProjectNotFoundError("Project does not exist.")

    memberships = ProjectMembership.objects.filter(project_id=project_id).values(
        "id", "user_id", "project_id", "role"
    )

    return [
        ProjectMembershipListDTO(
            id=str(membership["id"]),
            user_id=str(membership["user_id"]),
            project_id=str(membership["project_id"]),
            role=membership["role"],
        )
        for membership in memberships
    ]
