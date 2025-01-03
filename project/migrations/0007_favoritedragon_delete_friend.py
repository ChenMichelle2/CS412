# Generated by Django 5.1.3 on 2024-12-05 21:03

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0006_rename_added_on_friend_timestamp_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="FavoriteDragon",
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
                ("added_on", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "dragon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorited_by",
                        to="project.dragon",
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorites",
                        to="project.profile",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Friend",
        ),
    ]
