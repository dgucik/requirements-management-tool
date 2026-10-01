from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectCreateMembershipDTO:
    """Serialized owner membership data returned by project creation."""

    id: str
    user_id: str
    project_id: str
    role: str


@dataclass(frozen=True)
class ProjectCreateDTO:
    """Serialized project data returned after project creation."""

    id: str
    name: str
    owner_membership: ProjectCreateMembershipDTO


@dataclass(frozen=True)
class ProjectUpdateDTO:
    """Serialized project data returned after a project update."""

    id: str
    name: str


@dataclass(frozen=True)
class ProjectListDTO:
    """Serialized project data returned by the project list selector."""

    id: str
    name: str
    role: str


@dataclass(frozen=True)
class ProjectMembershipCreateDTO:
    """Serialized membership data returned after membership creation."""

    id: str
    user_id: str
    project_id: str
    role: str


@dataclass(frozen=True)
class ProjectMembershipUpdateDTO:
    """Serialized membership data returned after a membership update."""

    id: str
    user_id: str
    project_id: str
    role: str
