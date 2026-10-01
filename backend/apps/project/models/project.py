from django.db import models

from core.models import BaseModel


class Project(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
