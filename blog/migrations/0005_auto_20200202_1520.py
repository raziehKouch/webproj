# Generated by Django 2.2.9 on 2020-02-02 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200131_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('comment_pic', models.ImageField(blank=True, null=True, upload_to='comment_picd')),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='chanel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Chanel'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_pic',
            field=models.ImageField(blank=True, null=True, upload_to='post_picd'),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
            ],
        ),
    ]
