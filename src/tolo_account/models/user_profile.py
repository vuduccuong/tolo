from django.contrib.auth import get_user_model
from django.db import models


class UserProfile(models.Model):
    first_name = models.CharField(blank=False, max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=False)
    avatar = models.CharField(max_length=1000, null=True)
    birthday = models.DateTimeField()
    bio = models.TextField(null=True, default="")
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=False,
    )

    def __str__(self):
        return f"{self.user.id}-{self.user.email}: {self.first_name} {self.middle_name} {self.last_name}"

    class Meta:
        db_table = "tolo_user_profiles"
