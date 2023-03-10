# Generated by Django 4.1.5 on 2023-01-07 06:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("middle_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("avatar", models.CharField(max_length=1000, null=True)),
                ("birthday", models.DateTimeField()),
                ("bio", models.TextField(default="", null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "tolo_user_profiles",
            },
        ),
    ]
