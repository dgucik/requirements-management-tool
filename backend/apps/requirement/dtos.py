from dataclasses import dataclass


@dataclass(frozen=True)
class RequirementVersionCreateDTO:
    """Serialized first requirement version data returned after creation."""

    id: str
    requirement_id: str
    title: str
    description: str
    status: str
    version: int
    feature_id: str


@dataclass(frozen=True)
class RequirementCreateDTO:
    """Serialized requirement and first version data returned after creation."""

    id: str
    key: str
    first_version: RequirementVersionCreateDTO
