# Generated by Django 2.2.9 on 2020-02-02 15:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0012_auto_20200202_1807'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='follow',
            new_name='subscribe',
        ),
    ]
