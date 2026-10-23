from .dtos import ProjectListDTO, ProjectMembershipListDTO
from .exceptions import ProjectNotFoundError
from .models import Project, ProjectMembership


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


def project_user_can_create_feature(*, project_id: str, user_id: str) -> bool:
    """Check whether a user may create features in a project.

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
