from ..dtos import ProjectListDTO
from ..models import Project


def project_list(*, user_id: str) -> list[ProjectListDTO]:
    """Return projects where the user has a membership.

    Args:
        user_id: Identifier of the user whose projects should be returned.

    Returns:
        Projects accessible to the user, including the user's role in each project.
    """

    memberships = Project.objects.filter(
        memberships__user_id=user_id,
    ).values("id", "name", "memberships__role")

    return [
        ProjectListDTO(
            id=str(membership["id"]),
            name=membership["name"],
            role=membership["memberships__role"],
        )
        for membership in memberships
    ]
