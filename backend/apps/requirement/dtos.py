from dataclasses import dataclass


@dataclass(frozen=True)
class RequirementInitialVersionDTO:
    """Serialized first requirement version data returned after creation."""

    id: str
    requirement_id: str
    based_on_version_id: str | None
    created_by_id: str | None
    title: str
    description: str
    status: str
    version: int
    feature_id: str
    target_release_version_id: str | None
    implemented_release_version_id: str | None


@dataclass(frozen=True)
class RequirementCreateDTO:
    """Serialized requirement and first version data returned after creation."""

    id: str
    key: str
    first_version: RequirementInitialVersionDTO


@dataclass(frozen=True)
class RequirementListDTO:
    """Flattened requirement data combined with its latest active version."""

    id: str
    key: str
    version_id: str
    based_on_version_id: str | None
    created_by_id: str | None
    title: str
    description: str
    status: str
    version: int
    feature_id: str
    target_release_version_id: str | None
    implemented_release_version_id: str | None


@dataclass(frozen=True)
class FeatureCreateDTO:
    """Serialized feature data returned after creation."""

    id: str
    key: str
    title: str
    project_id: str


@dataclass(frozen=True)
class RequirementVersionCreateDTO:
    """Serialized requirement version returned after creating a new version."""

    id: str
    requirement_id: str
    based_on_version_id: str
    created_by_id: str
    title: str
    description: str
    status: str
    version: int
    feature_id: str
    target_release_version_id: str | None
    implemented_release_version_id: str | None
