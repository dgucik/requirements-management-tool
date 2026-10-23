from core.exceptions import (
    BusinessRuleError,
    EntityNotFoundError,
    PermissionDeniedError,
)


class RequirementCreationForbiddenError(PermissionDeniedError):
    """Raised when a user cannot create requirements in a project."""


class RequirementUpdateForbiddenError(PermissionDeniedError):
    """Raised when a user cannot update requirements in a project."""


class RequirementFeatureNotFoundError(EntityNotFoundError):
    """Raised when the selected feature does not belong to the project."""


class RequirementNotFoundError(EntityNotFoundError):
    """Raised when a requirement does not exist in the selected project."""


class RequirementReleaseVersionNotFoundError(EntityNotFoundError):
    """Raised when a referenced release version does not exist."""


class RequirementTitleRequiredError(BusinessRuleError):
    """Raised when a requirement has no title."""


class RequirementDescriptionRequiredError(BusinessRuleError):
    """Raised when a requirement has no description."""


class FeatureCreationForbiddenError(PermissionDeniedError):
    """Raised when a user cannot create features in a project."""


class FeatureTitleRequiredError(BusinessRuleError):
    """Raised when a feature is created without a non-empty title."""
