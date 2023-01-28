from django.contrib.auth import get_user_model
from django.db import models

from tolo_core.abstract_models.permalink import Permalinkable
from tolo_core.abstract_models.publish import Publishable
from tolo_core.abstract_models.timestamp import Timestampable
from tolo_core.abstract_models.user_interaction import UserInteractionable

User = get_user_model()


class Post(
    Timestampable,
    UserInteractionable,
    Publishable,
    Permalinkable,
    models.Model,
):
    title = models.CharField(max_length=200)
    description = models.CharField(blank=True, default="", max_length=500)
    content = models.TextField()
    thumbnail = models.TextField()
    author = models.ForeignKey(
        User, related_name="posts", on_delete=models.DO_NOTHING, null=True
    )

    class Meta:
        db_table = "tolo_posts"
