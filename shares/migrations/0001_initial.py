# Generated by Django 5.0.6 on 2024-06-19 08:49

import django.db.models.deletion
import shares.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Share",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "slug",
                    models.SlugField(
                        default=shares.models.default_slug,
                        max_length=15,
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "directory",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="Containing Directory"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="Shared File Name"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="share",
            constraint=models.UniqueConstraint(
                fields=("directory", "name"), name="unique_path"
            ),
        ),
    ]
