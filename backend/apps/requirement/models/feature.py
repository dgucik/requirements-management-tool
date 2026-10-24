from django.db import models

from core.models import BaseModel
from apps.project.models import Project


class Feature(BaseModel):
    """Group requirements under a project feature."""

    key = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="features",
        db_column="project_id",
    )

    def __str__(self):
        """Return the feature title."""

        return self.title
