# Generated by Django 5.0.6 on 2024-06-25 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shares", "0002_downloadlog"),
    ]

    operations = [
        migrations.AddField(
            model_name="share",
            name="download_enabled",
            field=models.BooleanField(default=True, verbose_name="Enable Download"),
        ),
    ]
