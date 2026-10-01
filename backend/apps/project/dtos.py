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


@dataclass(frozen=True)
class ProjectUpdateOutputDTO:
    """Serialized project data returned after a project update."""

    id: str
    name: str


@dataclass(frozen=True)
class ProjectListItemDTO:
    """Serialized project membership data returned in a project list."""

    id: str
    name: str
    role: str
