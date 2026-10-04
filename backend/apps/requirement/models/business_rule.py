from django.db import models

from core.models import BaseModel

from .requirement import Requirement


class BusinessRule(BaseModel):
    """Describe a business rule associated with one or more requirements."""

    key = models.SlugField(max_length=255, unique=True)
    rule = models.TextField()
    requirements = models.ManyToManyField(
        Requirement,
        related_name="business_rules",
        blank=True,
    )

    def __str__(self):
        """Return the business rule text."""

        return self.rule
