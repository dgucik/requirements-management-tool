from apps.project.dtos import ProjectListItemDTO
from apps.project.models import Project


def project_list(*, user_id: str) -> list[ProjectListItemDTO]:
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
        ProjectListItemDTO(
            id=str(membership["id"]),
            name=membership["name"],
            role=membership["memberships__role"],
        )
        for membership in memberships
    ]
