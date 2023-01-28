from django.db import models


class UserInteractionable(models.Model):
    created_by = models.PositiveIntegerField(default=0)
    updated_by = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
