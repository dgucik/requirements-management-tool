from core.exceptions import (
    BusinessRuleError,
    EntityNotFoundError,
    PermissionDeniedError,
)


class RequirementCreationForbiddenError(PermissionDeniedError):
    """Raised when a user cannot create requirements in a project."""


class RequirementVersionUpdateForbiddenError(PermissionDeniedError):
    """Raised when a user cannot update requirement versions in a project."""


class RequirementVersionNotEditableError(BusinessRuleError):
    """Raised when a requirement version cannot be edited by the requesting user."""


class RequirementVersionNotApprovedError(BusinessRuleError):
    """Raised when a new version is based on a version that is not approved."""


class RequirementFeatureNotFoundError(EntityNotFoundError):
    """Raised when the selected feature does not belong to the project."""


class RequirementNotFoundError(EntityNotFoundError):
    """Raised when a requirement does not exist in the selected project."""


class RequirementVersionNotFoundError(EntityNotFoundError):
    """Raised when the source version does not belong to the requirement."""


class RequirementReleaseVersionNotFoundError(EntityNotFoundError):
    """Raised when a referenced release version does not exist."""


class RequirementTitleRequiredError(BusinessRuleError):
    """Raised when a requirement version has no title."""


class RequirementDescriptionRequiredError(BusinessRuleError):
    """Raised when a requirement version has no description."""


class FeatureCreationForbiddenError(PermissionDeniedError):
    """Raised when a user cannot create features in a project."""


class FeatureTitleRequiredError(BusinessRuleError):
    """Raised when a feature is created without a non-empty title."""
