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
class FeatureListDTO:
    """Serialized feature data returned by the project feature selector."""

    id: str
    key: str
    title: str
    project_id: str


@dataclass(frozen=True)
class FeatureUpdateDTO:
    """Serialized feature data returned after an update."""

    id: str
    key: str
    title: str
    project_id: str


@dataclass(frozen=True)
class FeatureDeleteDTO:
    """Serialized result of soft-deleting a feature."""

    id: str
    is_deleted: bool


@dataclass(frozen=True)
class BusinessRuleCreateDTO:
    """Serialized business rule data returned after creation."""

    id: str
    key: str
    rule: str
    requirement_ids: list[str]


@dataclass(frozen=True)
class BusinessRuleListDTO:
    """Serialized business rule data returned by the project selector."""

    id: str
    key: str
    rule: str
    requirement_ids: list[str]


@dataclass(frozen=True)
class BusinessRuleUpdateDTO:
    """Serialized business rule data returned after an update."""

    id: str
    key: str
    rule: str
    requirement_ids: list[str]


@dataclass(frozen=True)
class BusinessRuleDeleteDTO:
    """Serialized result of soft-deleting a business rule."""

    id: str
    is_deleted: bool


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
