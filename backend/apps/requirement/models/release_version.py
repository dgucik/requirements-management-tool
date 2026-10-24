from django.db import models

from apps.project.models import Project
from core.models import BaseModel


class ReleaseVersion(BaseModel):
    """Represent a named product release to which requirements can be tied."""

    name = models.CharField(max_length=255, unique=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="release_versions",
        db_column="project_id",
    )

    def __str__(self):
        """Return the release version name."""

        return self.name
