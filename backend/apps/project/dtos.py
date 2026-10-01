from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectMembershipDTO:
    id: str
    user_id: str
    project_id: str
    role: str


@dataclass(frozen=True)
class ProjectCreateOutputDTO:
    id: str
    name: str
    owner_membership: ProjectMembershipDTO
