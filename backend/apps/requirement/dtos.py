from dataclasses import dataclass


@dataclass(frozen=True)
class RequirementCreateDTO:
    """Serialized requirement data returned after creation."""

    id: str
    key: str
    created_by_id: str
    title: str
    description: str
    feature_id: str
    target_release_version_id: str | None
    implemented_release_version_id: str | None


@dataclass(frozen=True)
class RequirementListDTO:
    """Serialized requirement data returned by the list selector."""

    id: str
    key: str
    created_by_id: str | None
    title: str
    description: str
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
class RequirementUpdateDTO:
    """Serialized requirement data returned after an update."""

    id: str
    key: str
    created_by_id: str | None
    title: str
    description: str
    feature_id: str
    target_release_version_id: str | None
    implemented_release_version_id: str | None


@dataclass(frozen=True)
class RequirementDeleteDTO:
    """Serialized result of soft-deleting a requirement."""

    id: str
    is_deleted: bool
