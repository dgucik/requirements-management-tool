from django.db import models
from django.conf import settings

from core.models import BaseModel

from .feature import Feature
from .release_version import ReleaseVersion


class Requirement(BaseModel):
    """Store a requirement and its current editable content."""

    key = models.SlugField(max_length=255, unique=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="created_requirements",
        db_column="created_by_id",
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    target_release_version = models.ForeignKey(
        ReleaseVersion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="target_requirements",
        db_column="target_release_version_id",
    )
    implemented_release_version = models.ForeignKey(
        ReleaseVersion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="implemented_requirements",
        db_column="implemented_release_version_id",
    )
    feature = models.ForeignKey(
        Feature,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="requirements",
        db_column="feature_id",
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        """Return the requirement key."""

        return self.key
