# Generated by Django 4.1.7 on 2023-03-03 20:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0006_userbookralation'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserBookRalation',
            new_name='UserBookRelation',
        ),
    ]
