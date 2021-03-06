# Generated by Django 3.1.7 on 2021-04-12 17:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0004_delete_favorite"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="favorite",
            field=models.ManyToManyField(
                related_name="favorite", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
