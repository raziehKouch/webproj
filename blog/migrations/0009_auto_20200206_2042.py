# Generated by Django 2.2.9 on 2020-02-06 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20200206_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_pic',
            field=models.ImageField(blank=True, height_field='50vw', null=True, upload_to='post_picd', width_field='50vw'),
        ),
    ]
