# Generated by Django 5.0 on 2024-04-11 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_post_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='filetype',
            field=models.CharField(default='img', max_length=10),
        ),
    ]
