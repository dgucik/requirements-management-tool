from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectMembershipDTO:
    """Serialized membership data returned by project operations."""

    id: str
    user_id: str
    project_id: str
    role: str


@dataclass(frozen=True)
class ProjectCreateOutputDTO:
    """Serialized project data returned after project creation."""

    id: str
    name: str
    owner_membership: ProjectMembershipDTO
