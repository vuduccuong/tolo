from django.db import models


class Timestampable(models.Model):
    """
    Abstract base class model that providers self-updating `created` and `modified`
    """

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
