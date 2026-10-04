from ..dtos import ProjectListDTO
from ..models import Project, ProjectMembership


def project_list(*, user_id: str) -> list[ProjectListDTO]:
    """Return projects where the user has a membership.

    Args:
        user_id: Identifier of the user whose projects should be returned.

    Returns:
        Projects accessible to the user, including the user's role in each project.
    """

    memberships = Project.objects.filter(
        memberships__user_id=user_id,
    ).values("id", "name", "code", "memberships__role")

    return [
        ProjectListDTO(
            id=str(membership["id"]),
            name=membership["name"],
            code=membership["code"],
            role=membership["memberships__role"],
        )
        for membership in memberships
    ]


def project_user_can_create_requirement(*, project_id: str, user_id: str) -> bool:
    """Check whether a user may create requirements in a project.

    Args:
        project_id: Identifier of the project to check.
        user_id: Identifier of the user whose permission is checked.

    Returns:
        True for project editors, moderators, and owners; otherwise False.
    """

    return ProjectMembership.objects.filter(
        project_id=project_id,
        user_id=user_id,
        role__in=[
            ProjectMembership.Role.EDITOR,
            ProjectMembership.Role.MODERATOR,
            ProjectMembership.Role.OWNER,
        ],
    ).exists()
