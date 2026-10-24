from core.exceptions import (
    BusinessRuleError,
    EntityNotFoundError,
    PermissionDeniedError,
)


class RequirementCreationForbiddenError(PermissionDeniedError):
    """Raised when a user cannot create requirements in a project."""


class RequirementUpdateForbiddenError(PermissionDeniedError):
    """Raised when a user cannot update requirements in a project."""


class RequirementDeleteForbiddenError(PermissionDeniedError):
    """Raised when a user cannot delete requirements in a project."""


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


class FeatureUpdateForbiddenError(PermissionDeniedError):
    """Raised when a user cannot update features in a project."""


class FeatureDeleteForbiddenError(PermissionDeniedError):
    """Raised when a user cannot delete features in a project."""


class FeatureNotFoundError(EntityNotFoundError):
    """Raised when an active feature does not belong to the project."""


class FeatureTitleRequiredError(BusinessRuleError):
    """Raised when a feature is created without a non-empty title."""


class BusinessRuleCreationForbiddenError(PermissionDeniedError):
    """Raised when a user cannot create business rules in a project."""


class BusinessRuleUpdateForbiddenError(PermissionDeniedError):
    """Raised when a user cannot update business rules in a project."""


class BusinessRuleDeleteForbiddenError(PermissionDeniedError):
    """Raised when a user cannot delete business rules in a project."""


class BusinessRuleNotFoundError(EntityNotFoundError):
    """Raised when an active business rule is not assigned to a project."""


class BusinessRuleRequirementsNotFoundError(EntityNotFoundError):
    """Raised when business rule requirements are not active in the project."""


class BusinessRuleTextRequiredError(BusinessRuleError):
    """Raised when a business rule has no text."""
